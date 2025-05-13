from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles