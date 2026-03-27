🍌 ComfyUI-GetToken-Banana
ComfyUI GetToken NanoBanana 终极生成器 是一款为中文用户量身定制的商业级 ComfyUI 插件。它完美接入了 GetToken 官方的 NanoBanana Pro 和 NanoBanana 2 图像大模型，将“文生图”与“图生图”无缝融为一体，并搭载了极速并发与抗网络波动的核心引擎。

API获取网址：https://nb.gettoken.cn/

✨ 核心特性 (Features)
🛡️ 突破 10MB 物理限制：首创“二进制流直传+短链替换”技术，完美绕过官方 API 请求体最大 10MB 的限制。无论你连入多大、多少张的高清垫图，都能顺滑提交，绝不卡顿！

🚀 多线程并发涡轮增压：彻底告别单张排队等待！支持 1-4 张图片同时发起并发请求，大幅缩短批量抽卡耗时。

🤖 智能路由双模合一：无需繁琐切换节点。

文生图：只写提示词，默认执行文生图。

图生图：只需将图片连入 垫图_x 接口，节点自动感应并无缝切换至图生图模式（最高支持 9 张图混合垫图）。

🏥 工业级容错与防弹网络架构：

伤员打捞机制：批量生成时，若某一张图因网络波动失败，自动剔除失败项并返回其余成功图片，绝不让整批任务陪葬。

抗 CDN 延迟：针对官方服务器内置渐进式退避算法（Exponential Backoff）与真实浏览器级 User-Agent 伪装，彻底解决 404 Not Found 及静态防盗链拦截问题。

🇨🇳 全中文沉浸式 UI：所有参数节点均已深度汉化，告别英语生词，并自带 ComfyUI 原生“高贵黄”专属皮肤。
<img width="1582" height="1172" alt="10cb1369ae5510cf3d62667c08eb624a" src="https://github.com/user-attachments/assets/c3d33937-47da-4a88-9d0e-fe52d8814a89" />

📦 安装指南 (Installation)
方法一：手动安装
下载本仓库，将文件夹重命名为 ComfyUI-GetToken-Banana。

将该文件夹放入你的 ComfyUI 插件目录：ComfyUI/custom_nodes/。

打开命令行终端，进入该插件目录，安装依赖：

Bash
cd ComfyUI/custom_nodes/ComfyUI-GetToken-Banana
pip install -r requirements.txt
重启 ComfyUI。

🛠️ 使用说明 (Usage)
在 ComfyUI 画布空白处双击或右键，搜索 GetToken，即可找到 🍌 GetToken NanoBanana 生成器节点。

参数详解
api_key: 必填。请在此处填入您在 GetToken 获取的 API 凭证。

模型: 提供 nano-banana-pro (精细度更高) 与 nano-banana-2 供选择。

提示词: 描述您想要生成的画面内容。

画面比例: 支持从 1:1 到 21:9 等多种主流画幅，选 auto 则由模型自由发挥。

图片尺寸: 控制输出精度，支持 1k, 2k, 4k。

生成数量: 一次性生成的图片张数（下拉选择 1~4 张，享受并发加速）。

seed: 随机种子。建议在 ComfyUI 的控制面板中将其设置为 randomize（随机），以确保每次生成不同的盲盒效果。

连线指南
如果你需要图生图（垫图），请使用 Load Image（加载图像）节点，将其连入本节点的 垫图_1。你可以最多连接 9 张不同的图片用于融合生成。

将本节点的 IMAGE 输出端连接至 Save Image（保存图像）或 Preview Image（预览图像）节点即可查看成品。

❓ 常见问题 (FAQ)
Q: 为什么控制台会提示“CDN暂未同步完成，等待 X 秒后重试”？ A: 这是正常现象。API 绘画速度极快，但云端服务器将生成的图片推送到可下载的静态 CDN 节点需要几秒钟的同步时间。插件会自动等待并安全重试，请耐心等候其下载完成。

Q: 生成多张图片时，为什么输出端少了一张？ A: 恭喜你触发了“容错保护机制”。这说明其中一张图片在下载时遇到了严重的网络阻断，插件为了保护已成功的图片不被销毁，自动跳过了那张失败的图。请检查您的本地代理网络（建议开启 TUN/全局路由模式）。

Q: 垫图时提示上传失败怎么办？ A: 请确保填写的 api_key 准确无误且账户余额充足。

📜 许可证 (License)
本项目仅供学习与技术交流使用。关于 NanoBanana 模型的生成内容与版权归属，请遵循 GetToken 官方相关服务条款。
