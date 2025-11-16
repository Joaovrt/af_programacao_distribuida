python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
pip install -r front/requirements.txt
pip install -r test/requirements.txt
cd backend python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/school.proto
python backend/grpc_server.py
python front/api.py
python test/test_api.py