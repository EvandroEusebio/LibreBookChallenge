 $(document).ready(function() {
        const form = $('#addBookForm');
        const formMessages = $('#form-messages');

        form.on('submit', function(e) {
            e.preventDefault(); // Impede o envio padrão do formulário

            formMessages.hide().removeClass('alert-success alert-danger').text(''); // Limpa mensagens anteriores

            // Coleta os dados do formulário
            const title = $('#title').val();
            const description = $('#description').val();
            const status = $('#status').val();

            // Validação simples
            if (!title) {
                showMessage('danger', 'Por favor, insira um título para o livro.');
                return;
            }

            // Desabilita o botão para evitar múltiplos envios
            const submitButton = form.find('.btn-submit');
            submitButton.prop('disabled', true).text('Criando...');

            frappe.call({
                method: 'libre.api.create_book_project',
                args: {
                    title: title,
                    description: description,
                    status: status,
                },
                callback: function(r) {
                    submitButton.prop('disabled', false).text('Criar Livro'); // Reabilita o botão

                    if (r.message) {
                        // Sucesso
                        showMessage('success', 'Livro criado com sucesso!');
                        window.location.href = `/mybooks`; 
                    } else {
                        const errorMessage = r.exc ? JSON.parse(r.exc)._error_message || 'Erro desconhecido' : 'Erro desconhecido';
                        showMessage('danger', `Erro: ${errorMessage}`);
                    }
                },
                error: function(err) {
                    submitButton.prop('disabled', false).text('Criar Livro'); // Reabilita o botão
                    showMessage('danger', `Erro de rede ou servidor: ${err.statusText || err}`);
                }
            });
        });

        function showMessage(type, message) {
            formMessages.text(message).addClass('alert-' + type).fadeIn();
        }
    });