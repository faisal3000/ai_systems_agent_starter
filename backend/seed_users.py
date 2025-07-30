from sqlmodel import SQLModel, Session, create_engine, select
from app.auth import User          # same model the API imports

engine = create_engine("sqlite:///./users.db", echo=False)
SQLModel.metadata.create_all(engine)

with Session(engine) as s:
    user = s.exec(select(User).where(User.email == "f.khann@gmail.com")).first()
    if user:
        user.password  = "Passw0rd!"
        user.is_active = True
        user.is_admin  = True
        msg = "updated"
    else:
        user = User(email="f.khann@gmail.com",
                    password="Passw0rd!",
                    is_active=True,
                    is_admin=True)
        s.add(user)
        msg = "created"
    s.commit()
    print(f"✅  Admin user {msg} in users.db")
