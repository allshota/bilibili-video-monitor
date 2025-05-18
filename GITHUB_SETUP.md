# GitHub 仓库设置指南

本文档提供了如何将此项目上传到 GitHub 的步骤指南。

## 初始化 Git 仓库

在项目根目录下执行以下命令：

```bash
# 初始化 Git 仓库
git init

# 添加所有文件到暂存区
git add .

# 提交初始代码
git commit -m "初始提交：B站视频监控系统"
```

## 连接到 GitHub

1. 在 GitHub 上创建一个新的仓库，不要初始化仓库（不添加 README、LICENSE 或 .gitignore 文件）

2. 连接本地仓库到 GitHub：

```bash
# 添加远程仓库地址（替换为您的 GitHub 用户名和仓库名）
git remote add origin https://github.com/你的用户名/bilibili-monitor.git

# 推送代码到 GitHub
git push -u origin main
```

如果您的默认分支是 master 而不是 main，请使用：

```bash
git push -u origin master
```

## 验证上传

1. 访问您的 GitHub 仓库页面，确认所有文件都已正确上传
2. 检查 GitHub Actions 是否已自动运行测试
3. 确认 README.md 文件中的徽章显示正确

## 后续维护

每次修改代码后，使用以下命令推送更新：

```bash
git add .
git commit -m "更新说明：简要描述您的更改"
git push
```

## 注意事项

- 确保您的 GitHub 账户已设置 SSH 密钥或使用个人访问令牌进行身份验证
- 如果您在推送时遇到权限问题，请检查您的 GitHub 凭据
- 定期更新您的依赖项并推送 requirements.txt 的更改