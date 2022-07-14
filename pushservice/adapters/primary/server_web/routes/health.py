from fastapi import APIRouter

router = APIRouter(
    tags=["Health"],
    responses={501: {"description": "Not implemented"}},
)


@router.get("/")
async def main():
    return {"data": "Hello World"}
