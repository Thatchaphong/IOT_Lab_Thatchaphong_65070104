from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils

#Book Table in Class

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    newbook = models.Book(title=book['title'], author=book['author'], year=book['year'],detail=book['detail'],story=book['story'],catagory=book['catagory'], is_published=book['is_published'])
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return newbook

@router_v1.patch('/books/{book_id}')
async def update_book(book_id: int, book: dict, db: Session = Depends(get_db)):
    db_item = db.query(models.Book).filter(models.Book.id == book_id).first()
    for key, value in book.items():
            setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    # response.status_code = 201
    return db_item

@router_v1.delete('/books/{book_id}')
async def delete_book(book_id: int,db: Session = Depends(get_db)):
    db_item = db.query(models.Book).filter(models.Book.id == book_id).first()
    db.delete(db_item)
    db.commit()
    return "Delete successfully"
    

#Students Table Assignments

@router_v1.get('/students')
async def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@router_v1.get('/students/{student_id}')
async def get_students(student_id: int, db: Session = Depends(get_db)):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

@router_v1.post('/students')
async def create_student(student: dict, response: Response, db: Session = Depends(get_db)):
    newstudent = models.Student(studentid=student['studentid'],firstname=student['firstname'], lastname=student['lastname'], birthdate=student['birthdate'], gender=student['gender'])
    db.add(newstudent)
    db.commit()
    db.refresh(newstudent)
    response.status_code = 201
    return newstudent

@router_v1.patch('/students/{student_id}')
async def update_student(student_id: int, student: dict, db: Session = Depends(get_db)):
    db_item = db.query(models.Student).filter(models.Student.id == student_id).first()
    for key, value in student.items():
            setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router_v1.delete('/students/{student_id}')
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Student).filter(models.Student.id == student_id).first()
    db.delete(db_item)
    db.commit()
    return "Delete successfully"

# Coffee Menu

@router_v1.get('/menus')
async def get_menu(db: Session = Depends(get_db)):
    return db.query(models.Menu).all()

@router_v1.get('/menus/{menu_id}')
async def get_menu(menu_id: int, db: Session = Depends(get_db)):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()

@router_v1.post('/menus')
async def create_menu(menu: dict, response: Response, db: Session = Depends(get_db)):
    newmenu = models.Menu(name=menu['name'], quantity=menu['quantity'], note=menu['note'], price=menu['price'])
    db.add(newmenu)
    db.commit()
    db.refresh(newmenu)
    response.status_code = 201
    return newmenu

@router_v1.patch('/menus/{menu_id}')
async def update_menu(menu_id: int, menu: dict, db: Session = Depends(get_db)):
    db_item = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    for key, value in menu.items():
            setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router_v1.delete('/menus/{menu_id}')
async def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    db.delete(db_item)
    db.commit()
    return "Delete successfully"

# Order menu

@router_v1.get('/orders')
async def get_order(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@router_v1.get('/orders/{order_id}')
async def get_order(order_id: int, db: Session = Depends(get_db)):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

@router_v1.post('/orders')
async def create_order(order: dict, response: Response, db: Session = Depends(get_db)):
    neworder = models.Order(name=order['name'], quantity=order['quantity'], note=order['note'], price=order['price'])
    db.add(neworder)
    db.commit()
    db.refresh(neworder)
    response.status_code = 201
    return neworder

@router_v1.patch('/orders/{order_id}')
async def update_order(order_id: int, order: dict, db: Session = Depends(get_db)):
    db_item = db.query(models.Order).filter(models.Order.id == order_id).first()
    for key, value in order.items():
            setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router_v1.delete('/orders/{order_id}')
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Order).filter(models.Order.id == order_id).first()
    db.delete(db_item)
    db.commit()
    return "Delete successfully"

app.include_router(router_v1)
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
