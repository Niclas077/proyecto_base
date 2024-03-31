
class Responses:
    @staticmethod
    def login_success(username):
          return f'''
        <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
        <script>
        Swal.fire("SweetAlert2 is working!").then(function() {{
            window.location.href = "/admin.html";
        }});
        </script>
        '''
    