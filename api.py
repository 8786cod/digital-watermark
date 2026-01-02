from flask import Flask, request, jsonify
import time
import hashlib
import os

app = Flask(__name__)

def is_valid_watermark_format(watermark: str) -> bool:
    """校验水印格式是否为GH:project-id"""
    if not watermark or not isinstance(watermark, str):
        return False
    return watermark.startswith("GH:") and len(watermark) >= 4  # GH:xxx 最小长度

def log_verification(watermark: str):
    """记录水印验证事件，自动创建GitHub Issue"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    issue_title = f"[verification] {watermark} - {timestamp}"
    issue_body = f"""
## Watermark Verification Record
- Watermark Content: {watermark}
- Timestamp (UTC): {timestamp}
- Verified via: /verify API
- Auto-Generated: Yes
"""
    print(f"=== GitHub Issue: {issue_title} ===")
    print(issue_body)
    print("=====================================")
    # 实际实现可调用GitHub API创建Issue（同stego_core.py）

@app.route('/verify', methods=['GET'])
def verify_watermark():
    """
    水印验证API接口（公开可访问，用于开源项目版权验证）
    支持两种参数：watermark（直接传入水印）、hash（传入水印MD5哈希）
    返回JSON格式验证结果
    """
    # 获取请求参数
    watermark = request.args.get('watermark')
    hash_str = request.args.get('hash')
    # 参数校验
    if not watermark and not hash_str:
        return jsonify({"error": "Missing parameter: watermark or hash"}), 400
    
    # 初始化验证结果
    verification_result = {
        "request_time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        "valid": False,
        "message": "Invalid watermark or hash"
    }
    
    # 场景1：直接传入水印
    if watermark:
        if not is_valid_watermark_format(watermark):
            verification_result["error"] = "Invalid watermark format (must start with GH:)"
            return jsonify(verification_result), 400
        # 模拟验证（实际需解析图片提取水印，此处为业务逻辑骨架）
        project_id_short = watermark[3:].replace('-', '/')
        verification_result.update({
            "watermark": watermark,
            "valid": True,
            "detection_method": "Five-Point Sampling",
            "project_url": f"https://github.com/{project_id_short}",
            "verification_url": request.url,
            "message": "Watermark is valid"
        })
        # 记录验证事件
        log_verification(watermark)
        return jsonify(verification_result)
    
    # 场景2：传入水印哈希
    if hash_str:
        # 模拟哈希校验（实际需关联水印数据库）
        verification_result.update({
            "hash": hash_str,
            "valid": True,
            "detection_method": "Five-Point Sampling",
            "evidence_url": f"https://your-repo.netlify.app/evidence/{hash_str}",
            "message": "Hash corresponds to a valid watermark"
        })
        return jsonify(verification_result)
    
    return jsonify(verification_result), 400

# 本地运行入口
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
