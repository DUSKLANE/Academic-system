# 山东交通学院教务系统逆向工程

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/Status-已完成-green.svg)](https://github.com/your-repo)

山东交通学院教务系统的自动化登录和数据获取工具，支持成绩查询、课表查询等功能。

## 🎯 功能特性

### 🔐 核心功能
- **智能登录**：自动获取登录页面参数，支持动态加密密钥
- **会话管理**：维护登录状态，支持后续数据请求
- **数据解析**：自动解析HTML页面，提取结构化数据
- **错误处理**：完善的异常处理和重试机制

### 📊 数据获取
- **成绩查询**：获取所有课程成绩信息（课程名称、学分、成绩、考试时间等）
- **课表查询**：支持按日期查询课表和学期理论课程表
- **课程详情**：课程安排、上课时间、教室、教师等信息

## 🛠️ 技术实现

### 加密算法
- **AES-ECB模式**：用于密码加密
- **Base64编码**：数据编码处理
- **动态密钥**：从登录页面动态获取加密密钥

## 🔧 使用方法

### 基本登录

```python
from sdjt import Login

# 创建登录实例
username = "your_student_id"  # 学号
password = "your_password"     # 密码
login = Login(username, password)

# 检查登录状态
if login.islogin:
    print("登录成功！")
    print(f"当前会话: {login.session}")
else:
    print("登录失败！")
```

### 获取成绩信息

```python
from sdjt import getAllScore

# 确保已登录
if login.islogin:
    # 获取所有成绩
    scores = getAllScore(login.session)
```

### 获取课表信息

#### 获取本周课表

```python
from sdjt import getWeekTimetable

# 获取本周课表
timetable = getWeekTimetable(login.session)

```

#### 获取指定日期课表

```python
import datetime

# 获取指定日期的课表
specific_date = datetime.date(2024, 1, 15)
timetable = getWeekTimetable(login.session, specific_date)
```

## 🔒 安全注意事项

- **账号安全**：不要在代码中硬编码密码，建议使用环境变量或配置文件
- **使用频率**：避免频繁请求，建议设置合理的请求间隔
- **数据隐私**：妥善保管获取的学术数据，不要泄露给他人
- **合规使用**：仅用于个人学习研究，遵守学校相关规定

---

**注意**：本工具仅供学习和研究使用，请遵守学校相关规定，合理使用教务系统资源。
