## Backend

Backend for EZPark


ezpart_backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoint1.py
│   │   ├── endpoint2.py
│   │   └── ...（Endpoints）
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── auth.py
│   │   └── ...（utils）
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── ...（models）
│   └── config/
│       ├── __init__.py
│       └── settings.py
├── tests/
│   ├── __init__.py
│   ├── test_endpoint1.py
│   └── ...（更多测试文件）
├── requirements.txt
├── README.md
└── .env
