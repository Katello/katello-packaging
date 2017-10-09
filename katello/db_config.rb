require 'yaml'

module KatelloUtilities
  class DBConfig
    attr_reader :foreman, :candlepin
    INSTALLER_CONFIG = '/etc/foreman-installer/scenarios.d/last_scenario.yaml'

    def initialize(scenario = INSTALLER_CONFIG)
      config = YAML.load(File.read(scenario))
      answers = YAML.load(File.read(config[:answer_file]))
      @foreman = {
          :username => answers['foreman']['db_username'],
          :password => answers['foreman']['db_password'],
          :database => answers['foreman']['db_database'] || 'foreman',
          :host => answers['foreman']['db_host'] || 'localhost',
          :port => answers['foreman']['db_port'] || '5432'
      }
      @candlepin = {
          :username => answers['katello']['candlepin_db_user'],
          :password => answers['katello']['candlepin_db_password'],
          :database => answers['katello']['candlepin_db_name'] || 'candlepin',
          :host => answers['katello']['candlepin_db_host'] || 'localhost',
          :port => answers['katello']['candlepin_db_port'] || '5432',
          :ssl => answers['katello']['candlepin_ssl'] || false,
          :ssl_verify => answers['katello']['candlepin_ssl_verify'] || false
      }
    end

    def remote_db?(config)
      !['localhost', '127.0.0.1', `hostname`.strip].include? config[:host]
    end

    def any_local_db?
      !remote_db?(foreman) || !remote_db?(candlepin)
    end

    def any_remote_db?
      remote_db?(foreman) || remote_db?(candlepin)
    end

    def pg_command(config, command, args)
      "PGPASSWORD='#{config[:password]}' #{command} -U #{config[:username]} -h #{config[:host]} -p #{config[:port]} -d #{config[:database]} #{args}"
    end

    def pg_dump_command(config, dump_file)
      "PGPASSWORD='#{config[:password]}' pg_dump -U #{config[:username]} -h #{config[:host]} -p #{config[:port]} -Fc #{config[:database]} > #{dump_file}"
    end
  end
end
