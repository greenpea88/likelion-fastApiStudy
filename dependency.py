from typing import Optional

from fastapi import Depends, FastAPI, Cookie, Header, HTTPException

app = FastAPI()


#dependency 사용
def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    #dependency injection을 통해서 매번 parameter를 입력하지 않고 함수를 통해서 간단히 작성할 수 있게됨.
    return {"q": q, "skip": skip, "limit": limit}



@app.get("/items/")
def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
def read_users(commons: dict = Depends(common_parameters)):
    return commons

#---------------------------------------------------------
#class를 dependency로 활용하기
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonQueryParams:

    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        #클래스의 인스턴스를 생성하는 생성자
        self.q = q

        self.skip = skip

        self.limit = limit



@app.get("/classitems/")
def read_class(
        commons: CommonQueryParams = Depends(CommonQueryParams)
        # commons: Depends(CommonQueryParams) #위처럼 말고 다음과 같이 간결하게 작성도 가능
):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

#---------------------------------------------------------
#sub-dependency : dependency 내부에 dependency를 다시금 선언
def query_extractor(q: Optional[str] = None):
    return q


def query_or_cookie_extractor(

    q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)

):
    if not q:
        return last_query
    return q


@app.get("/query/")
def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}

def sub_dep_int(q: Optional[int] = None):
    return q

def dep_str(
        q: int = Depends(sub_dep_int), qq: Optional[str] = None
):
    if not q:
        return qq
    return q

@app.get("/subdep/")
def subdep(query: int = Depends(dep_str)):
    #dep_str의 return 타입이 서로 다른 경우 error가 발생하지 않는가?
    # -> dep_str의 return type에 대해 fast api의 체킹이 안되고 파이썬으로 넘어가게 되는 것으로 추정
    return {"test": query}

#---------------------------------------------------------
#path operation decorator에 dependency 사용하기
async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key



@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def pathop():
    return [{"item": "Foo"}, {"item": "Bar"}]
