# libre/www/add_chapter.py
import frappe
from frappe import _

def get_context(context):
    project_name = frappe.form_dict.get('project_name') # Pega o project_name da rota
    print("Project Name:", project_name)
    if not project_name:
        frappe.throw(_("Nome do projeto não especificado."), frappe.ValidationError)

    try:
        book_project = frappe.get_doc("BookProject", project_name)
        # Verifica se o usuário logado é o autor para permitir a edição
        if book_project.autor != frappe.session.user:
            frappe.throw(_("Você não tem permissão para adicionar capítulos a este livro."), frappe.PermissionError)

        context.book_project = book_project
        context.title = _(f"Adicionar Capítulo a: {book_project.titulo}")
    except frappe.DoesNotExistError:
        frappe.throw(_(f"Livro '{project_name}' não encontrado."), frappe.DoesNotExistError)
    except frappe.PermissionError as e:
        frappe.throw(e.message, frappe.PermissionError)
    except Exception as e:
        frappe.log_error(frappe.utils.get_traceback(), "Error fetching BookProject for add_chapter page")
        frappe.throw(_(f"Ocorreu um erro ao carregar a página: {e}"))