"""
部署到Snowflake Streamlit的辅助脚本
"""

import os
import shutil
from pathlib import Path

def prepare_snowflake_deployment():
    """准备Snowflake部署所需的文件"""

    print("=" * 60)
    print("准备Snowflake Streamlit部署")
    print("=" * 60)
    print()

    # 创建部署目录
    deploy_dir = Path("./snowflake_deploy")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()

    print("1. 创建部署目录...")
    print(f"   ✓ {deploy_dir}")
    print()

    # 复制必要文件
    print("2. 复制必要文件...")

    files_to_copy = [
        "streamlit_gemini.py",
        "requirements_gemini.txt",
        "environment.yml",
    ]

    for file in files_to_copy:
        src = Path(file)
        if src.exists():
            shutil.copy(src, deploy_dir / file)
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} (未找到)")

    # 复制src目录
    src_dir = Path("src")
    if src_dir.exists():
        shutil.copytree(src_dir, deploy_dir / "src")
        print(f"   ✓ src/")
    else:
        print(f"   ✗ src/ (未找到)")

    print()

    # 修改streamlit_gemini.py以适配Snowflake
    print("3. 修改streamlit_gemini.py以适配Snowflake...")
    streamlit_file = deploy_dir / "streamlit_gemini.py"

    if streamlit_file.exists():
        with open(streamlit_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 在文件开头添加Snowflake适配代码
        snowflake_header = '''"""
Gemini Smart RAG - Snowflake Streamlit版本
"""

import streamlit as st
import os

# Snowflake适配: 使用secrets而不是.env
def get_google_api_key():
    """从Snowflake secrets或环境变量获取API密钥"""
    try:
        # 尝试从Snowflake secrets获取
        return st.secrets["GOOGLE_API_KEY"]
    except:
        # 回退到环境变量
        return os.getenv("GOOGLE_API_KEY")

# 覆盖原来的环境变量获取
os.environ['GOOGLE_API_KEY'] = get_google_api_key() or ""

# 使用临时目录存储数据库
SNOWFLAKE_TEMP_DIR = "/tmp/gemini_smart_rag_db"

'''

        # 插入header
        if "import streamlit as st" not in content[:200]:
            content = snowflake_header + "\n" + content
        else:
            # 替换import语句后的部分
            import_idx = content.find("import streamlit as st")
            next_line = content.find("\n", import_idx) + 1
            content = content[:next_line] + snowflake_header + content[next_line:]

        # 保存修改后的文件
        with open(streamlit_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print("   ✓ 已添加Snowflake适配代码")
    else:
        print("   ✗ streamlit_gemini.py未找到")

    print()

    # 创建README
    print("4. 创建Snowflake部署说明...")
    readme_content = """# Snowflake部署说明

## 部署步骤

### 1. 登录Snowflake
访问: https://app.snowflake.com/

### 2. 创建Streamlit App
1. 点击 "Streamlit" → "Create"
2. 选择 "From scratch"

### 3. 上传文件
将以下文件上传到Snowflake:
- `streamlit_gemini.py` (主应用文件)
- `src/` (整个文件夹)
- `environment.yml` (依赖配置)

### 4. 配置Secrets
在Snowflake Streamlit设置中添加:

```toml
GOOGLE_API_KEY = "your-google-api-key-here"
```

获取API密钥: https://aistudio.google.com/apikey

### 5. 部署
点击 "Deploy" 按钮，等待1-2分钟即可完成。

## 注意事项

1. **数据持久化**:
   - Snowflake使用临时存储(`/tmp`)
   - 应用重启时数据会丢失
   - 建议预先索引好数据库并上传

2. **上传预索引数据库**:
   ```bash
   # 本地索引
   python index_gemini.py

   # 导出数据库
   python database_manager.py export ./gemini_smart_rag_db db.tar.gz

   # 将db.tar.gz上传到Snowflake Stage
   ```

3. **性能考虑**:
   - 首次查询可能较慢（冷启动）
   - 建议使用小型测试数据集

## 常见问题

**Q: 数据库丢失怎么办？**
A: 使用Snowflake Stage存储预索引的数据库，启动时自动加载。

**Q: 如何更新应用？**
A: 直接在Snowflake UI中编辑文件，保存后自动重新部署。

**Q: 支持多用户吗？**
A: 支持，但所有用户共享同一个数据库。
"""

    readme_file = deploy_dir / "SNOWFLAKE_README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print("   ✓ SNOWFLAKE_README.md")
    print()

    # 完成
    print("=" * 60)
    print("✓ 准备完成！")
    print("=" * 60)
    print()
    print("部署文件位置:")
    print(f"  {deploy_dir.absolute()}")
    print()
    print("下一步:")
    print("  1. 访问 https://app.snowflake.com/")
    print("  2. 上传 snowflake_deploy/ 中的文件")
    print("  3. 配置 GOOGLE_API_KEY secret")
    print("  4. 点击 Deploy")
    print()
    print("详细说明请查看:")
    print(f"  {readme_file.absolute()}")
    print()


if __name__ == "__main__":
    prepare_snowflake_deployment()
