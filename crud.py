import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select
from sqlalchemy.orm import joinedload, selectinload

from core.models import db_helper, User, Profile, Post


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    print("user", user)
    await session.commit()


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none()
    user: User | None = await session.scalar(stmt)
    print(f"{user=}")
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None,
    last_name: str | None,
) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    return profile


# async def show_users_with_profiles(session: AsyncSession) -> list[User]:
#     stmt = select(User).order_by(User.id)
#     # result: Result = await session.execute(stmt)
#     # users = result.scalars()
#     users = await session.scalars(stmt)
#     for user in users:
#         print(user)
#         print(user.profile.first_name) ошибка не подгружен профиль


async def show_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        if user.profile:
            print(user.profile.first_name)


async def create_post(
    session: AsyncSession,
    user_id: int,
    post_titles: tuple[str, ...],
) -> list[Post]:
    posts = [
        Post(title=title, user_id=user_id)
        for title in post_titles
    ]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts

async def get_users_with_posts(
        session: AsyncSession
) -> list[User]:
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = select(User).options(
            # joinedload(User.posts),
            selectinload(User.posts) # подгружает все посты отдельно
        ).order_by(User.id)
    # users = await session.scalars(stmt)
    result: Result = await session.execute(stmt)
    # users = result.unique().scalars()
    users = result.scalars()

    # for user in users.unique():
    for user in users:
        print("*" * 20)
        print(user)
        for post in user.posts:
            print("-", post)


async def get_posts_with_authors(
        session: AsyncSession
) -> list[Post]:
    stmt = select(Post).options(
            joinedload(Post.user),
        ).order_by(Post.id)
    # result: Result = await session.execute(stmt)
    # posts = result.scalars()
    posts = await session.scalars(stmt)
    for post in posts:
        print("post", post)
        print("author", post.user)
      
        

async def get_users_with_posts_and_profiles(
        session: AsyncSession
) -> list[User]:
    stmt = select(User).options(
            joinedload(User.profile),
            selectinload(User.posts)
        ).order_by(User.id)
    
    users = await session.scalars(stmt)
    for user in users:
        print("*" * 20)
        # print(user)
        # if user.profile:
        #     print(user.profile.first_name)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)

async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        .where(User.username == "xuebes")
        .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)

async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session, "pedoras")
        # await create_user(session, "neger")
        # await create_user(session, "xuebes")
        user_xuebes = await get_user_by_username(session, "xuebes")
        user_neger = await get_user_by_username(session, "neger")
        # # await get_user_by_username(session, "dayn")
        # await create_user_profile(
        #     session=session,
        #     user_id=user_xuebes.id,
        #     first_name="Xuesos",
        #     last_name="Xuesos"
        # )
        # await create_user_profile(
        #     session=session,
        #     user_id=user_neger.id,
        #     first_name="Shadow",
        #     last_name=""
        # )
        # await show_users_with_profiles(session=session)
        # await create_post(
        #     session=session,
        #     user_id=user_neger.id,
        #     post_titles = ("Жопа", 'dota2', 'sigma')
        # )
        # await create_post(
        #     session=session,
        #     user_id=user_xuebes.id,
        #     post_titles = ("cs2 govno", 'dota2 govno', 'sigma top')
        # )
        # await get_users_with_posts(session=session)
        # await get_posts_with_authors(session=session)
        # await get_users_with_posts_and_profiles(session=session)
        await get_profiles_with_users_and_users_with_posts(session=session)

if __name__ == "__main__":
    asyncio.run(main())
