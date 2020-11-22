import shutil
from datetime import datetime
from typing import Union
from pathlib import Path
from fastapi import UploadFile

from src.database.base import engine, Session
from src.models.store import StoreModel, Base
from src.models.users import User
from src.utils import get_random_filename, project_root, static_path, base_url


Base.metadata.create_all(engine)

store_table = StoreModel.__table__


# Add a new file into the database
async def post_file(file: UploadFile, user: User) -> Union[str, None]:
    try:
        filename = Path(get_random_filename(with_subdirs=True))
        suffixes = Path(file.filename).suffixes
        if len(suffixes) > 0:
            base = filename.parent
            name = filename.name
            for suffix in suffixes:
                name += suffix
            filename = base / name
        relative_path = static_path() / filename
        absolute_path = project_root() / relative_path
        if not absolute_path.parent.is_dir():
            absolute_path.parent.mkdir(parents=True, exist_ok=True)

        # get file
        with open(str(absolute_path), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        url = f"{base_url()}/store/{filename}"
        # put record to db
        store_row = StoreModel(
            user_id=user.id,
            email=user.email,
            enterdate=datetime.now(),
            filename=file.filename,
            url=str(url),
            path= str(relative_path)
        )
        session = Session()
        session.add(store_row)
        session.commit()
        session.close()
        return url
    except Exception as e:
        print("exception", e)
        return None


# Delete a file from the database
async def delete_file(url: str, user: User) -> bool:

    session = Session()
    store_row = session.query(StoreModel).filter_by(url=url, user_id=user.id).first()
    if store_row is not None:
        absolute_path = project_root() / store_row.path
        absolute_path.unlink(missing_ok=True)
        session.delete(store_row)
        session.commit()
        session.close()
        return True
    else:
        return False
