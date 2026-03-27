import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "GetToken.Banana.ThemeColor",
    nodeCreated(node) {
        // 当画布上创建节点时，检查是不是咱们的“🍌生成器”
        if (node.comfyClass === "GetToken_Banana_Ultimate") {
            // 设定为 ComfyUI 原生面板标准黄色的 Hex 颜色码
            node.color = "#443221";     // 标题栏颜色
            node.bgcolor = "#665534";   // 节点背景颜色
        }
    }
});