import frappe
from frappe import _
from frappe.utils import nowdate

@frappe.whitelist()
def get_full_book(project_name: str):
    user = frappe.session.user

    if user == "Guest":
        frappe.throw(_("Autenticação necessária."), frappe.AuthenticationError)

    # Verifica se o projeto existe e pertence ao usuário autenticado
    if not frappe.db.exists("BookProject", {"name": project_name, "autor": user}):
        frappe.throw(_("Projeto não encontrado ou você não tem permissão."), frappe.PermissionError)
    
    if not frappe.db.exists("BookProject", project_name):
        frappe.throw(_("Projeto não encontrado."), frappe.DoesNotExistError)

    project = frappe.get_doc("BookProject", project_name)

    chapters = frappe.get_all(
        "BookChapter",
        filters={"refbookprojectrefbookproject": project.titulo},
        fields=["ordem", "titulo", "conteudo"],
    )

    return {
        "project": {
            "title": project.titulo,
            "description": project.descricao,
            "author": project.autor,
            "data_de_criacao": project.data_de_criacao,
            "status": project.status,
        },
        "chapters": chapters
    }

@frappe.whitelist() 
def create_book_project(title, description, status="publicado"):

    if frappe.session.user == "Guest":
        frappe.throw("Você precisa estar logado para criar um livro.", frappe.PermissionError)

    try:
        book_project = frappe.get_doc({
            "doctype": "BookProject",
            "titulo": title,
            "descricao": description,
            "data_de_criaco": nowdate(), # Garante que a data é a de hoje
            "autor": frappe.session.user, 
            "status": status,
            "published": 1
        })
        book_project.insert(ignore_permissions=False) # Garante que as permissões são respeitadas
        frappe.db.commit() 
        return book_project.name
    except Exception as e:
        frappe.log_error(frappe.utils.get_traceback(), "Error creating BookProject via API")
        frappe.throw(f"Erro ao criar o livro: {e}")


@frappe.whitelist()
def create_chapter(project_name, title, order, content):
    if frappe.session.user == "Guest":
        frappe.throw("Você precisa estar logado para adicionar um capítulo.", frappe.PermissionError)

    try:
        # Verifica se o BookProject existe e se o usuário logado é o autor
        book_project = frappe.get_doc("BookProject", project_name)
        if book_project.autor != frappe.session.user:
            frappe.throw("Você não tem permissão para adicionar capítulos a este livro.", frappe.PermissionError)
        print("Creating chapter for project:", project_name)
        print("Creating chapter for project:", order)
        print("Creating chapter for project:", title)
        print("Creating chapter for project:", content)
        
        chapter = frappe.get_doc({
            "doctype": "BookChapter",
            "refbookprojectrefbookproject": project_name,
            "titulo": title,
            "ordem": order,
            "conteudo": content
        })
        chapter.insert(ignore_permissions=False)
        frappe.db.commit()

        return chapter.titulo # Retorna o nome do novo capítulo

    except Exception as e:
        frappe.log_error(frappe.utils.get_traceback(), "Error creating Chapter via API")
        frappe.throw(f"Erro ao criar o capítulo: {e}")
