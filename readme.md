Vagrant.configure(2) do |config|
  config.ssh.insert_key = false
  config.vbguest.auto_update = true
  config.ssh.forward_x11 = true

  config.vm.define "receptor" do |web_config|
    web_config.vm.box = "ubuntu/trusty64"
    web_config.vm.hostname = "receptor"
    web_config.vm.network "private_network", ip: "192.168.56.21"
    web_config.vm.synced_folder ".", "/home/vagrant"
    web_config.vm.provider "virtualbox" do |vb|
      vb.name = "receptor"
      opts = ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize opts
      vb.memory = "256"
    end
    web_config.vm.provision "shell", inline: <<-SHELL
      # Instalar dependências
      sudo apt-get update
      sudo apt-get install -y python3 python3-pip gcc
      # Opcional: instalar outros pacotes necessários
    SHELL
  end

  config.vm.define "remetente" do |client_config|
    client_config.vm.box = "ubuntu/trusty64"
    client_config.vm.hostname = "remetente"
    client_config.vm.network "private_network", ip: "192.168.56.11"
    client_config.vm.synced_folder ".", "/home/vagrant"
    client_config.vm.provider "virtualbox" do |vb|
      vb.name = "remetente"
      opts = ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize opts
      vb.memory = "256"
    end
    client_config.vm.provision "shell", inline: <<-SHELL
      # Instalar dependências
      sudo apt-get update
      sudo apt-get install -y python3 python3-pip gcc
      # Opcional: instalar outros pacotes necessários
    SHELL
  end
end