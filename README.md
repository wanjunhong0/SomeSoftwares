# 预研方向服务器远程开发指南

## 简介
在我们日常工作中，经常性的需要通过SSH的协议，远程连接服务器进行算法的开发测试等活动。
目前绝大多数关于远程开发的文档，包括公司内部，网上的资料等都主要还是面向开发以及测试方向的工作编写的。
而预研方向的工作与开发或者测试的工作有显著的区别，导致一定程度上上诉的资料并不适用预研的场景。

- 开发和测试方向工作主要重在远程服务器上部署运行相关程序；而预研工作则是主要重在利用远程服务器的硬件资源加速、并行化、和多进程的能力
- 开发和测试方向工作侧重于环境的配置和兼容性；而预研工作则不太需要关注这些
- 开发和测试方向工作的指标是程序的成功运行，所以一般的编程语言的log反馈就能满足其需求；而预研工作的指标是算法的性能指标，一般的log可能无法满足其全部需求，需要debug等工具来辅助

目前SSH远程开发的工具的使用流行度如下图，由vs code studio占据了一半以上的份额，并且经我使用，发现其确实优于其他几个选项，所以接下来我将详细介绍其功能和使用方法。

![stats](https://github.com/wanjunhong0/SomeSoftwares/blob/master/stats.png)


 **Visual Studio Code Remote - SSH**
是一款基于VS Code的插件允许你在任何远程机器、虚拟机或容器上打开一个远程文件夹，并充分利用 VS Code IDE的功能。连接到远程服务器，你就可以与远程文件系统上任何位置的文件和文件夹进行交互。因为插件直接在远程机器上运行命令和其他扩展，因此无需在本地机器上放置源代码，也不吃本机的配置性能（适合我们无盘机远程服务器开发的特性）。
使用VS Code远程开发可以提供类似于本地质量的开发体验，包括IDE界面、代码导航、调试和Debug。

![SSH Architecture](https://github.com/microsoft/vscode-docs/blob/main/docs/remote/images/ssh/architecture-ssh.png)

[插件官方文档](https://code.visualstudio.com/docs/remote/ssh-tutorial)


## **VS Code Remote SSH** 优点

- 传统SSH远程和开发所需的IDE是分离的，**VS Code Remote SSH**统一了二者
- 通常大家通过**Putty**或者**Xshell**的软件远程只能返回Terminal界面，无法满足现在复杂的开发需求
- **Pycharm**等IDE虽然也具备远程功能，但是在能本机编辑，实时上传调试，而不像**VS Code Remote SSH**可以直接在远程主机上编辑调试
- **VS Code** 本体小巧，不吃本机配置，运行速度快
- **VS Code** 是近来年最受欢迎的IDE



### 系统要求

**本机:**  只许安装 [兼容 OpenSSH 的 SSH 客户端](/docs/remote/troubleshooting.md#installing-a-supported-ssh-client)

**远程 SSH 主机**: [SSH 服务器](/docs/remote/troubleshooting.md#installing-a-supported-ssh-server) 需要:

- x86_64 Debian 8+, Ubuntu 16.04+, CentOS / RHEL 7+
- ARMv7l (AArch32) Raspberry Pi OS  Stretch/9+ (32-bit)
- ARMv8l (AArch64) Ubuntu 18.04+ (64-bit)
- Windows 10 / Server 2016/2019 (1803+) 需要 [Windows 官方 OpenSSH 客户端](https://docs.microsoft.com/windows-server/administration/openssh/openssh_install_firstuse)
- macOS 10.14+ (Mojave) SSH 主机需要 [Remote Login enabled](https://support.apple.com/guide/mac-help/allow-a-remote-computer-to-access-your-mac-mchlp1066/mac).
- 远程主机需要至少1 GB 内存, 但是双核CPU推荐至少2 GB 内存以上

其他基于`glibc` x86_//64、ARMv7l (AArch32) 和 ARMv8l (AArch64) 的 Linux 发行版如果具有所需的先决条件，应该也可以运行。有关行社区支持的信息和提示，请参阅[使用 Linux 进行远程开发](/docs/remote/linux.md)。

虽然 ARMv7l (AArch32) 和 ARMv8l (AArch64) 支持可用，但由于在扩展中使用 x86 本机代码，安装在这些设备上的某些扩展可能无法正常工作。

### 安装

1. 如果尚未安装[兼容 OpenSSH 的 SSH 客户端](/docs/remote/troubleshooting.md#installing-a-supported-ssh-client)，请安装该客户端。

2. 安装 [Visual Studio Code](https://code.visualstudio.com/) or [Visual Studio Code Insiders](https://code.visualstudio.com/insiders/)。

3. 安装 [远程开发扩展包](https://aka.ms/vscode-remote/download/extension)。

### SSH主机设置

1. 如果你还没有设置 SSH 主机，请按照 [Linux](/docs/remote/troubleshooting.md#installing-a-supported-ssh-server), [Windows 10 / Server (1803+)](https://docs.microsoft.com/windows-server/administration/openssh/openssh_install_firstuse), 和 [macOS](https://support.apple.com/guide/mac-help/allow-a-remote-computer-to-access-your-mac-mchlp1066/mac) SSH 主机的说明进行操作，或者在 Azure 上创建一个 [VM on Azure](https://docs.microsoft.com/azure/virtual-machines/linux/quick-create-portal?toc=%2fazure%2fvirtual-machines%2flinux%2ftoc.json)。

2. **可选:** 如果您的 Linux 或 macOS SSH 主机将被多个用户同时访问，请考虑在 VS Code用户设置中启用 **Remote.SSH: Remote Server Listen On Socket** 中的 [User settings](/docs/getstarted/settings.md) 以提高安全性。

    在设置编辑器中：

    ![Listen on socket VS Code setting](ssh-listen-on-socket.png)

    有关详细信息，请参阅 [Tips and Tricks](/docs/remote/troubleshooting.md#improving-security-on-multi-user-servers)。

3. **可选:** 虽然支持基于密码的身份验证，但我们建议为主机设置 **key based authentication** 。 有关详细信息，请参阅 [Tips and Tricks](/docs/remote/troubleshooting.md#configuring-key-based-authentication)。

### 连接到远程主机

要首次连接到远程主机，请执行以下步骤：

1. 通过从Terminal/PowerShell 窗口中运行以下命令来验证您是否可以连接到 SSH 主机，并根据需要进行替换 `user@hostname`。

    ```bash
    ssh user@hostname
    # Or for Windows when using a domain / AAD account
    ssh user@domain@hostname
    ```

2. 在 VS Code 中，从命令面板（F1、Ctrl+Shift+P ）中选择**Remote-SSH: Connect to Host...** 并使用与步骤 1 相同的方法`user@hostname`。

    ![Illustration of user@host input box](ssh-user@box.png)

3. 如果 VS Code 无法自动检测到正在连接的服务器类型，则会要求手动选择。

    ![Illustration of platform selection](ssh-select-platform.png)

    选择平台后，它将存储在 [VS Code settings](/docs/getstarted/settings.md)  `remote.SSH.remotePlatform` 因此您可以随时更改它。

4. 之后 VS Code 将连接到 SSH 服务器并自行设置。VS Code 将使用进度通知最新状态，您可以在 `Remote - SSH` 输出通道中看到详细的日志。

    > **提示:** 连接挂起或失败？有关解决常见问题的信息，请参阅 [故障排除提示](/docs/remote/troubleshooting.md#troubleshooting-hanging-or-failing-connections)。
    >
    > 如果您看到有关 SSH 文件权限的错误，请参阅 [修复 SSH 文件权限错误](/docs/remote/troubleshooting.md#fixing-ssh-file-permission-errors)。

5. 连接上后，您将处于一个空白的窗口中。你可以参考状态栏来查看您连接到的主机。

    ![SSH Status bar item](ssh-statusbar.png)

    单击状态栏项目将在您连接时提供远程命令列表。

6. 然后，您可以像在本地一样使用 **File > Open...** 或者 **File > Open Workspace...** 打开远程计算机上的任何文件夹或工作区。

    ![File Open on a remote SSH host](ssh-open-folder.png)

从这里，你可以在远程主机时使用的任何扩展包并开始编辑。

> **注意:** 在 ARMv7l / ARMv8l `glibc` SSH 主机上，某些扩展包可能无法工作，因为扩展包中包含 x86 编译的本机代码。

### 在 Docker 中打开远程 SSH 主机上的文件夹

如果您使用的是 Linux 或 macOS SSH 主机，则可以一起使用 Remote - SSH 和 Remote - Containers 扩展包在 Docker 内的远程主机上打开文件夹。你甚至不需要在本地安装 Docker 客户端。

为此:

1. 按照远程主机上的 Remote - Containers 扩展包的[安装步骤](/docs/remote/containers.md#installation)进行操作。
2. **可选:** 为服务器设置 [SSH 密钥的身份验证](/docs/remote/troubleshooting.md#configuring-key-based-authentication)，无需多次输入密码。
3. 按照 Remote - SSH 扩展的[快速入门](#connect-to-a-remote-host)连接到主机并在那里打开一个文件夹。
4. 使用命令面板中的 **Remote-Containers: Reopen in Container** 命令 (`kbstyle(F1)`, `kb(workbench.action.showCommands)`).

### 断开与远程主机的连接

要在完成远程主机上的文件编辑后关闭连接，请选择 **File > Close Remote Connection** 以断开与主机的连接。默认配置不包括此命令的键盘快捷键。你也可以简单地退出 VS Code 来关闭远程连接。

### 记住主机和高级设置

如果你有一组经常使用的主机，或者需要使用一些附加选项连接到主机，你可以将它们添加到遵循 [SSH 配置文件格式](https://man7.org/linux/man-pages/man5/ssh_config.5.html)的本地文件中。

为了简化设置，扩展程序可以帮助你添加主机，而无需手动编辑此文件。

首先从命令面板选择 **Remote-SSH: Add New SSH Host...** (`kbstyle(F1)`, `kb(workbench.action.showCommands)`) 或单击活动栏的 **Remote Explorer** 中选择 **Add New** 图标。

![Remote Explorer Add New item](ssh-explorer-add-new.png)

然后将要求你输入 SSH 连接信息。你可以输入主机名：

![Remote Explorer SSH host input](ssh-host-input.png)

或者用 `ssh` 从命令行连接到主机的完整命令:

![Remote Explorer SSH command input](ssh-command-input.png)

最后，系统会要求你选择要使用的配置文件。如果你想使用与列出的配置文件不同的配置文件，还可以在用户文件中设置`"remote.SSH.configFile"`中的`settings.json`。

例如 `ssh -i ~/.ssh/id_rsa-remote-ssh yourname@remotehost.yourcompany.com` 在输入框中输入将生成以下条目:

```text
Host remotehost.yourcompany.com
    User yourname
    HostName another-host-fqdn-or-ip-goes-here
    IdentityFile ~/.ssh/id_rsa-remote-ssh
```

从现在开始，当你从命令面板(`kbstyle(F1)`, `kb(workbench.action.showCommands)`)或 **Remote Explorer** 中的 **SSH Targets** 选择Remote-SSH: Connect to Host...时，主机将出现在主机列表中。

![SSH targets in the Remote Explorer](ssh-explorer-connect.png)

**Remote Explorer** 允许你在远程主机上打开一个新的空窗口或直接打开你之前打开的文件夹。展开主机并单击要在主机上打开的文件夹旁边的 **Open Folder** 图标。

![Remote Explorer open folder](ssh-explorer-open-folder.png)

## 管理扩展包

VS Code 在以下两个位置之一运行扩展：本地在 UI / 客户端，或远程在 SSH 主机上。虽然影响 VS Code UI 的扩展包（如主题和代码片段）安装在本地，但大多数扩展将驻留在 SSH 主机上。这可确保你获得流畅的体验，并允许你从本地计算机上为 SSH 主机上的给定工作区安装任何需要的扩展包。这样，你可以从另一台带有扩展程序的机器上准确地从上次中断的地方继续。

如果你从`Extensions` 视图安装扩展包，它将自动安装在正确的位置。安装后，你可以根据类别分组判断扩展包的安装位置。

您的远程 SSH 主机将有一个类别:

![Workspace Extension Category](ssh-installed-remote-indicator.png)

还有一个 **Local - Installed** 类别:

![Local Extension Category](local-installed-extensions.png)

实际需要远程运行的本地扩展包将在 **Local - Installed** 类别中显示为灰色和禁用。选择 **Install** 以在远程主机上安装扩展包。

![Disabled Extensions w/Install Button](ssh-disabled-extensions.png)

### “始终安装”扩展包

如果你希望在任何 SSH 主机上始终安装一些扩展，可以使用 `remote.SSH.defaultExtensions` property in `settings.json`。 例如，如果想安装 [GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens) 和 [Resource Monitor](https://marketplace.visualstudio.com/items?itemName=mutantdino.resourcemonitor) 扩展包, 请指定它们的扩展包 ID，如下所示:

```json
"remote.SSH.defaultExtensions": [
    "eamodio.gitlens",
    "mutantdino.resourcemonitor"
]
```

## 转发端口/创建 SSH 隧道

有时在开发时，你可能需要访问远程机器上的其他端口。有两种方法可以使用 [SSH tunnel](https://www.ssh.com/ssh/tunneling/example) 将所需的远程端口转发到本机。

### 临时转发端口

连接到主机后，如果你想在会话期间 **temporarily forward** 到新端口，请从命令面板(`kbstyle(F1)`, `kb(workbench.action.showCommands)`) 中选择 **Forward a Port** 或单击中的转发新端口图标从活动栏中选择 **Remote Explorer**。

![Remote Explorer forward port button](ssh-explorer-forward-port.png)

系统会要求输入要转发的端口，你可以为其命名。

![Forward port input](forward-port-ssh.png)

### 总是转发一个端口

如果你有固定的转发的端口, 你可以用 `LocalForward` 中的 [remember hosts and advanced settings](#remember-hosts-and-advanced-settings) 的同一个 SSH 配置文件中使用该指令。

例如，如果你想转发端口 3000 和 27017，可以按如下方式更新文件：

```text
Host remote-linux-machine
    User myuser
    HostName remote-linux-machine.mydomain
    LocalForward 127.0.0.1:3000 127.0.0.1:3000
    LocalForward 127.0.0.1:27017 127.0.0.1:27017
```

### 疑问

- 官方文档 [Tips and Tricks](/docs/remote/troubleshooting.md#ssh-tips) 和 [FAQ](/docs/remote/faq.md).
- 联系我：`万骏泓` 研究院\大数据智能部\大数据算法部\知识挖掘组
- 内网邮箱 wanjunhong@hikvision.com
- 外网邮箱 wanjunhong@hikvision.com
