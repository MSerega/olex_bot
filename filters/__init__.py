from filters.filters import IsLink, IsAdmin
from loader import dp

dp.filters_factory.bind(IsLink)
dp.filters_factory.bind(IsAdmin)
