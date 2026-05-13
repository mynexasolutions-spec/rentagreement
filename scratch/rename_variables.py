import os

files = [
    'static/css/base.css',
    'static/css/home.css',
    'static/css/pages.css',
    'static/css/components.css',
    'static/css/navbar.css',
    'static/css/footer.css',
    'templates/calculator.html',
    'templates/admin.html',
    'templates/faq.html',
    'templates/form.html',
    'templates/contact.html',
    'templates/index.html',
    'templates/base.html'
]

for f in files:
    path = os.path.join(r'c:\Users\Asus\Desktop\rentagreement', f)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        new_content = content.replace('--slate-', '--zinc-').replace('var(--slate-', 'var(--zinc-')
        
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Updated {f}")
