Vagrant.configure(2) do |config|
  config.ssh.insert_key = false
  config.vbguest.auto_update = true
  config.ssh.forward_x11 = true

  config.vm.define "file-receiver" do |receiver_config|
    receiver_config.vm.box = "ubuntu/trusty64"
    receiver_config.vm.hostname = "file-receiver"
    receiver_config.vm.network "private_network", ip: "192.168.56.21"
    receiver_config.vm.synced_folder ".", "/home/vagrant"
    receiver_config.vm.provider "virtualbox" do |vb|
      vb.name = "file-receiver"
      opts = ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize opts
      vb.memory = "256"
    end
    # Add this line to run the provisioner
    receiver_config.vm.provision "shell", inline: <<-SHELL
      # Instalar dependências
      sudo apt-get update
      sudo apt-get install -y python3 python3-pip gcc
      # Opcional: instalar outros pacotes necessários
    SHELL
  end

  config.vm.define "file-sender" do |sender_config|
    sender_config.vm.box = "ubuntu/trusty64"
    sender_config.vm.hostname = "file-sender"
    sender_config.vm.network "private_network", ip: "192.168.56.11"
    sender_config.vm.synced_folder ".", "/home/vagrant"
    sender_config.vm.provider "virtualbox" do |vb|
      vb.name = "file-sender"
      opts = ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize opts
      vb.memory = "256"
    end
    # Add this line to run the provisioner
    sender_config.vm.provision "shell", inline: <<-SHELL
      # Instalar dependências
      sudo apt-get update
      sudo apt-get install -y python3 python3-pip gcc
      # Opcional: instalar outros pacotes necessários
    SHELL
  end
end