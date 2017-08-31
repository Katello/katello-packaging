module KatelloUtilities
  module Helper
    def last_scenario
      File.basename(File.readlink("/etc/foreman-installer/scenarios.d/last_scenario.yaml")).split(".")[0]
    end

    def accepted_scenarios
      @accepted_scenarios || ["katello", "foreman-proxy-content"]
    end

    def error_message
      "This utility can't run on a non-katello system."
    end

    def run_cmd(command, exit_codes=[0], message=nil)
      result = `#{command}`
      unless exit_codes.include?($?.exitstatus)
        STDOUT.puts result
        STDOUT.puts message if message
        failed_command = "Failed '#{command}' with exit code #{$?.exitstatus}"
        if self.respond_to? :cleanup
          STDOUT.puts failed_command
          cleanup($?.exitstatus)
        end
        fail_with_message(failed_command)
      end
      result
    end

    def timestamp
      DateTime.now.strftime('%Y%m%d%H%M%S')
    end

    def fail_with_message(message, opt_parser=nil)
      STDOUT.puts message
      puts opt_parser if opt_parser
      exit(false)
    end
  end
end
