FROM python:3.11

# Create user with UID 1000 (Hugging Face requirement)
RUN useradd -m -u 1000 user
 
# Set environment variables for the non-root user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH
 
# Set working directory (creates /home/user/app automatically)
WORKDIR $HOME/app
 
# (Optional) If you want to disable pip caching entirely, you can skip creating the cache directory.
# Otherwise, you could fix its permissions—but here we opt to disable caching.
RUN mkdir -p $HOME/.cache

# Adjust ownership/permissions for the app directory (and /usr if needed)
RUN chown -R 1000:0 $HOME/app $HOME/.cache /usr && \
    chmod -R 777 $HOME/app /usr $HOME/.cache
    
COPY . $HOME/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

CMD ["python", "-m", "bot"]