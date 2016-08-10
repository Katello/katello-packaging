#!/usr/bin/env ruby

require 'optparse'

options = {
  :jenkins_job_id => 'lastSuccessfulBuild'
}

OptionParser.new do |opts|
  opts.banner = "Usage: release_package.rb [options]"

  opts.on("-p", "--project [PROJECT]", "Project to build an RPM for") do |project|
    options[:project] = project
  end

  opts.on("-r", "--releaser REQUIRED", "Tito releaser to release for") do |releaser|
    options[:releaser] = releaser
  end

  opts.on("--jenkins-job [JENKINS_JOB]", "Name of Jenkins job to pull source file from") do |job|
    options[:jenkins_job] = job
  end

  opts.on("--jenkins-job-id [JENKINS_JOB_ID]", "ID of Jenkins job to pull source from (default: lastSuccessfulBuild") do |id|
    options[:jenkins_job_id] = id unless id.nil?
  end
end.parse!

raise OptionParser::MissingArgument, "--project" if options[:project].nil?
raise OptionParser::MissingArgument, "--releaser" if options[:releaser].nil?

def log(msg)
  puts
  puts "== #{msg} =="
end

log("Initializing git annex")
puts `git-annex init`

log("Setting up source")
if options[:project] == 'rubygem-katello' || options[:project] == 'katello-installer'
  `./setup_sources.sh #{options[:project]} --relaxed`
else
  `./setup_sources.sh #{options[:project]}`
end

Dir.mkdir("rel-eng/build") if !File.exist?('rel-eng/build')

args = ["-o #{Dir.pwd}/rel-eng/build/"]

if (jenkins_job = options[:jenkins_job])
  args.push("--arg jenkins_job=#{jenkins_job}")

  if (jenkins_job_id = options[:jenkins_job_id])
    args.push("--arg jenkins_job_id=#{jenkins_job_id}")
  end
end

output = ''
Dir.chdir(options[:project]) do
  log("Running tito release for #{options[:project]} using #{options[:releaser]}")
  puts "tito release #{args.join(' ')} #{options[:releaser]}"
  output = `tito release #{args.join(' ')} #{options[:releaser]}`
  puts output
end

if (error = output.include?('ERROR'))
  puts output
  exit 1
end

if (traceback = output.include?('Traceback'))
  puts output
  exit 1
end

release_tasks = output.
                  split("\n").
                  select { |line| line.start_with?("Task info:") }.
                  collect { |line| line.scan(/\d+/) }.
                  flatten
release_count = release_tasks.length

if !release_tasks.empty?
  release_tasks = release_tasks.join(' ')
  log("Watching koji tasks #{release_tasks}")
  response = `koji -c ~/.koji/katello-config watch-task #{release_tasks}`
end

if $? == 0
  puts response
  exit 0
else
  build_exists_count = response.count("Build already exists") if response

  if build_exists_count == release_count
    exit 0
  else
    puts response
    exit 1
  end
end
