from src import api
from src.resources.jobs import (
    UserJobApi,
    UserJobDetailApi, 
    JobApi
)
from src.resources.responses import UserResponseDetailApi
from src.resources.users import UserApi
from src.resources.resumes import (
    ResumeApi, 
    ResumeDetailApi
)
from src.resources.auth import AuthRegister
from src.resources.auth import AuthLogin


api.add_resource(AuthRegister, '/auth/register/', strict_slashes=True)
api.add_resource(AuthLogin, '/auth/login/', strict_slashes=True)
api.add_resource(ResumeDetailApi, '/users/resumes/<int:resume_id>/', strict_slashes=False)
api.add_resource(ResumeApi, '/users/resumes/', strict_slashes=True)
api.add_resource(UserResponseDetailApi, '/users/responses/<int:job_id>/', strict_slashes=False)
api.add_resource(UserJobDetailApi, '/users/jobs/<int:job_id>/', strict_slashes=False)
api.add_resource(UserJobApi, '/users/jobs/', strict_slashes=False)
api.add_resource(JobApi, '/jobs/', '/jobs/<int:id>/', strict_slashes=False)
api.add_resource(UserApi, '/users/<int:id>/', strict_slashes=False)
