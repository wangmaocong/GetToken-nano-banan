import os
import time
import torch
import requests
import numpy as np
from PIL import Image
import io
import concurrent.futures

# ==========================================
# 核心 API 交互工具类
# ==========================================
class GetTokenClient:
    BASE_URL = "https://nb.gettoken.cn/openapi/v1"
    
    @staticmethod
    def tensor_to_bytes(tensor):
        i = 255. * tensor.cpu().numpy().squeeze()
        if len(i.shape) == 2:
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        else:
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()

    @staticmethod
    def upload_image(api_key, image_tensor):
        if image_tensor is None: return None
        url = f"{GetTokenClient.BASE_URL}/media/upload/binary"
        headers = {"Authorization": f"Bearer {api_key}"}
        files = {"file": ("input.png", GetTokenClient.tensor_to_bytes(image_tensor), "image/png")}
        
        try:
            resp = requests.post(url, headers=headers, files=files, timeout=60)
            resp.raise_for_status()
            res = resp.json()
            if res.get("code") == 0:
                return res["data"]["download_url"]
        except Exception as e:
            print(f"[GetToken Error] 图片上传失败: {e}")
        return None

    @staticmethod
    def poll_result(api_key, task_id, task_idx=1, total=1):
        query_url = f"{GetTokenClient.BASE_URL}/query"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        prefix = f"[GetToken | 图 {task_idx}/{total}]"
        
        while True:
            try:
                resp = requests.post(query_url, headers=headers, json={"taskId": task_id}, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                status = data.get("status")
                
                if status == "SUCCESS":
                    img_url = data["results"][0]["url"]
                    img_data = None
                    
                    # 高强度网络抗干扰装甲
                    for attempt in range(3):
                        try:
                            img_resp = requests.get(img_url, timeout=60) 
                            img_resp.raise_for_status()
                            img_data = img_resp.content
                            break
                        except Exception as dl_e:
                            print(f"\n{prefix} 警告: 图片下载被网络中断，重试 ({attempt+1}/3)... 错误: {dl_e}")
                            time.sleep(3)
                    
                    if not img_data:
                        raise Exception(f"{prefix} 连续 3 次下载失败，请检查网络/代理状态！")

                    image = Image.open(io.BytesIO(img_data)).convert("RGB")
                    image_np = np.array(image).astype(np.float32) / 255.0
                    print(f"{prefix} ✅ 下载完成！")
                    return torch.from_numpy(image_np)[None,]
                
                if status in ["FAILED", "TIMEOUT"]:
                    error_info = data.get('errorMessage', '未知错误')
                    tips = data.get('promptTips', '')
                    raise Exception(f"{prefix} ❌ 生成失败: {error_info}. {tips}")
                
                print(f"{prefix} 正在处理中 (状态: {status})...")
                time.sleep(3) 
            except Exception as e:
                if "生成失败" in str(e) or "下载失败" in str(e): 
                    raise e
                print(f"{prefix} ⚠️ 网络波动，等待恢复: {e}")
                time.sleep(5)

# ==========================================
# 终极合体节点：并发 + 容错 + 中文UI
# ==========================================
class GetTokenBananaNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": "", "placeholder": "在此粘贴您的 GetToken API Key"}),
                "模型": (["nano-banana-pro", "nano-banana-2"], {"default": "nano-banana-pro"}),
                "提示词": ("STRING", {"multiline": True, "default": ""}),
                "画面比例": (["auto", "1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3", "5:4", "4:5", "21:9"],),
                "图片尺寸": (["1k", "2k", "4k"], {"default": "1k"}),
                "生成数量": (["1", "2", "3", "4"], {"default": "1"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "操作说明": ("STRING", {
                    "multiline": True, 
                    "default": "💡 智能路由提示：\n1. 未连接图片时：默认执行【文生图】模式。\n2. 连接了图片时：自动切换为【图生图】模式。\n※ 提示框仅作说明，无需更改文本。"
                }),
            },
            "optional": {
                f"图像_{i}": ("IMAGE",) for i in range(1, 10)
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "GetToken/Banana"

    def generate(self, api_key, seed, **kwargs):
        if not api_key or api_key.strip() == "":
            raise Exception("【错误】请先输入您的 API Key！")

        # 提取动态中文参数
        model = kwargs.get("模型", "nano-banana-pro")
        prompt = kwargs.get("提示词", "")
        aspect_ratio = kwargs.get("画面比例", "auto")
        image_size = kwargs.get("图片尺寸", "1k")
        batch_count = int(kwargs.get("生成数量", "1"))

        # 图生图垫图只需要上传一次
        image_urls = []
        for i in range(1, 10):
            img_tensor = kwargs.get(f"图像_{i}")
            if img_tensor is not None:
                u = GetTokenClient.upload_image(api_key, img_tensor)
                if u: image_urls.append(u)
        
        is_i2i = len(image_urls) > 0
        is_pro = "pro" in model.lower()
        
        ver_path = "banana_pro" if is_pro else "banana2"
        mode_path = "image-to-image" if is_i2i else "text-to-image"
        url = f"{GetTokenClient.BASE_URL}/{ver_path}/{mode_path}"
        
        print(f"\n[GetToken] 模式: {'图生图' if is_i2i else '文生图'} | 模型: {model} | 批量: {batch_count}张 (🚀 并发加速 + 🛡️ 容错拦截已开启)")

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        
        def process_single_task(b):
            current_seed = seed + b 
            payload = {
                "prompt": prompt,
                "resolution": image_size.lower(),
                "clientTaskId": f"comfy_{current_seed}_{int(time.time())}"
            }
            if aspect_ratio != "auto": payload["aspectRatio"] = aspect_ratio
            if is_i2i: payload["imageUrls"] = image_urls

            print(f"[GetToken | 图 {b+1}/{batch_count}] 正在提交任务...")
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            
            task_id = resp.json().get("taskId")
            if not task_id: raise Exception(f"[GetToken | 图 {b+1}/{batch_count}] 任务提交失败！")
            
            return GetTokenClient.poll_result(api_key, task_id, task_idx=b+1, total=batch_count)

        result_tensors = []
        
        # 核心多线程并发引擎 + 容错机制
        with concurrent.futures.ThreadPoolExecutor(max_workers=batch_count) as executor:
            futures = [executor.submit(process_single_task, b) for b in range(batch_count)]
            
            for future in futures:
                try:
                    tensor = future.result() 
                    result_tensors.append(tensor) 
                except Exception as e:
                    # 拦截报错！单张图失败自动跳过
                    print(f"\n[GetToken 容错拦截] ⚠️ 有一张图片生成或下载失败，已自动跳过该张图。原因: {e}")

        # 如果全部失败，抛出致命异常中断运行
        if len(result_tensors) == 0:
            raise Exception("【致命错误】本次请求的所有图片均生成或下载失败，请检查网络或日志！")

        # 将成功拉回来的图片动态拼接
        final_batch_tensor = torch.cat(result_tensors, dim=0)
        
        print(f"[GetToken] 🎉 并发批量任务结束！成功挽回并输出: {len(result_tensors)} / {batch_count} 张。\n")
        return (final_batch_tensor,)