from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StudentDocumentForm
from .models import StudentDocument

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = StudentDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.student = request.user
            doc.save()
            return redirect('document_list')
    else:
        form = StudentDocumentForm()
    
    return render(request, 'EXPfileUploading/upload.html', {'form': form})

@login_required
def document_list(request):
    documents = StudentDocument.objects.filter(student=request.user)
    return render(request, 'EXPfileUploading/list.html', {'documents': documents})

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def review_document(request, doc_id):
    document = StudentDocument.objects.get(id=doc_id)

    if request.method == 'POST':
        document.is_approved = 'approve' in request.POST
        document.score = request.POST.get('score', None)
        document.save()
        return redirect('admin_document_list')

    return render(request, 'EXPfileUploading/review.html', {'document': document})
