# 1. Use a lightweight Python image
FROM python:3.10-slim

# 2. Create a non-root user (Hugging Face Requirement)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory
WORKDIR /app

# 4. Copy requirements first (from your backend folder)
# We change ownership to our new user so it can read/write
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 5. Copy the rest of the project
# This includes /backend and /db
COPY --chown=user . .

# 6. Expose the port
EXPOSE 7860

# 7. Start the app
# Using your specific path to main.py
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "7860"]