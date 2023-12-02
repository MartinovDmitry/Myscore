import shutil
from fastapi import UploadFile, APIRouter

from tasks import process_pic

router = APIRouter(
    prefix='/images',
    tags=['Images load']
)


@router.post('/leagues')
async def add_league_image(
        file: UploadFile,
):
    image_path = f'static/images/{file.filename[:-4]}.webp'
    with open(image_path, 'wb+') as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(image_path)