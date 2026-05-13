FROM nginx:alpine

COPY . /usr/share/nginx/html

# 删除不需要的文件
RUN rm -rf /usr/share/nginx/html/.git \
           /usr/share/nginx/html/.venv \
           /usr/share/nginx/html/.idea \
           /usr/share/nginx/html/.vscode \
           /usr/share/nginx/html/scraper \
           /usr/share/nginx/html/docs \
           /usr/share/nginx/html/pic_readme \
           /usr/share/nginx/html/requirements.txt \
           /usr/share/nginx/html/.env.example \
           /usr/share/nginx/html/.gitignore \
           /usr/share/nginx/html/CLAUDE.md \
           /usr/share/nginx/html/Dockerfile \
           /usr/share/nginx/html/docker-compose.yml

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
