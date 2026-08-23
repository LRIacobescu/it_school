from typing import Optional

from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(min_length=2)
    description: str = ""
    price: float = Field(gt=0)
    category: str = Field(min_length=2)
    available: bool = True


class ProductUpdate(BaseModel):
    name: str = Field(min_length=2)
    description: str = ""
    price: float = Field(gt=0)
    category: str = Field(min_length=2)
    available: bool = True


class ProductPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2)
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    category: Optional[str] = Field(default=None, min_length=2)
    available: Optional[bool] = None

class CategoryCreate(BaseModel):
    name: str = Field(min_length=2)


class CategoryUpdate(BaseModel):
    name: str = Field(min_length=2)


class CategoryPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2)

class RestaurantCreate(BaseModel):
    name: str = Field(min_length=2)
    city: str = Field(min_length=2)
    rating: float = Field(ge=0, le=5)
    is_open: bool = True


class RestaurantUpdate(BaseModel):
    name: str = Field(min_length=2)
    city: str = Field(min_length=2)
    rating: float = Field(ge=0, le=5)
    is_open: bool = True


class RestaurantPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2)
    city: Optional[str] = Field(default=None, min_length=2)
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    is_open: Optional[bool] = None