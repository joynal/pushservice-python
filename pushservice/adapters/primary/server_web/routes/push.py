from fastapi import APIRouter

router = APIRouter(
    prefix="/push",
    tags=["Push"],
    responses={501: {"description": "Not implemented"}},
)


@router.get("/")
async def get_all():
    return {"data": "Hello World"}


@router.get("/{push_id}")
async def get_one(push_id: str):
    return {"data": push_id}


@router.post("/")
async def create():
    return {"data": "Hello World"}


@router.patch("/{push_id}")
async def update(push_id: str):
    return {"data": push_id}


@router.delete("/{push_id}")
async def delete(push_id: str):
    return {"data": push_id}
