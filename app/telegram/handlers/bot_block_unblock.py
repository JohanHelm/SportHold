from aiogram import Router, F
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.types import Message, ChatMemberUpdated
from loguru import logger
from sqlalchemy.future import select
from aiogram.enums.chat_type import ChatType
from app.domain.helpers.enums import UserStatus
from app.infra.db.models.user.schema import User
from app.telegram.utils.db_queries import set_user_status


router: Router = Router()
router.my_chat_member.filter(F.chat.type == ChatType.PRIVATE)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated, db_session):
    logger.info(f"User {event.from_user.id} block bot")
    await set_user_status(
        db_session=db_session, user_id=event.from_user.id, status=UserStatus.INACTIVE
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated, db_session):
    logger.info(f"User {event.from_user.id} unblock bot")
    await set_user_status(
        db_session=db_session, user_id=event.from_user.id, status=UserStatus.ACTIVE
    )
