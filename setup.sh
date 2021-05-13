mkdir -p ~/.streamlit/
echo “\
[general]\n\
email = \”m_heidt@web.de\”\n\
“ > ~/.streamlit/credentials.toml
echo “\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
“ > ~/.streamlit/config.toml
