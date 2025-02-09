from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import F
from teacherProfile.models import Student
from studentProfile.models import Document

def upload_achievement(request):
    if request.method == 'POST':
        record_book = request.POST.get('record_book', '').strip()
        
        try:
            student = Student.objects.get(record_book__iexact=record_book)
            category = request.POST['category']
            score = int(request.POST['score'])
            total_score = score * len(request.FILES.getlist('files'))
            
            Student.objects.filter(pk=student.pk).update(
                **{f'{category}_score': F(f'{category}_score') + total_score}
            )
            
            files = request.FILES.getlist('files')
            if not files:
                messages.error(request, 'Выберите файлы!')
                return redirect('loadFiles:upload')
            
            documents = [
                Document(
                    student=student,
                    category=category,
                    doc_type=request.POST['doc_type'],
                    achievement=request.POST['achievement'],
                    score=score,
                    file=file
                ) for file in files
            ]
            Document.objects.bulk_create(documents)
            
            messages.success(request, f'Добавлено {len(files)} файл(-ов)')
            return redirect('loadFiles:upload')
            
        except Student.DoesNotExist:
            messages.error(request, f'Студент "{record_book}" не найден')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
    
    return render(request, 'loadFiles/index.html')