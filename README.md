# EduStego: Open Source Digital Watermarking
**免费开源的数字水印工具，100% GitHub原生集成，无需服务器！**
[![GitHub Sponsors](https://img.shields.io/badge/自愿赞助-Sponsor%20Me-orange)](https://github.com/sponsors/8786cod)
[![GitHub Stars](https://img.shields.io/github/stars/8786cod/digital-watermark?style=social)](https://github.com/8786cod/digital-watermark)

## 功能特点
-  **完全免费**：无使用次数限制，无功能阉割
-  **零配置部署**：3行代码接入GitHub Actions
-  **兼容主流格式**：支持PNG/JPG/GIF，压缩后仍可验证
-  **五点取样验证**：基于LSB隐写的防伪水印，安全可靠

## 快速开始
1. **接入你的GitHub项目**：
   ```yaml
   # .github/workflows/watermark.yml
   name: Add Digital Watermark
   on: [push]
   jobs:
     watermark:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: 8786cod/digital-watermark@main
           with:
             project-id: ${{ github.repository }}
