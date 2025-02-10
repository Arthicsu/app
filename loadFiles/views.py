from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import F
from django.http import JsonResponse
import json
from studentProfile.models import Document
from teacherProfile.models import Student

def upload_achievement(request):
    if request.method == 'POST':
        record_book = request.POST.get('record_book', '').strip()
        
        if not record_book:
            messages.error(request, 'Номер зачетной книжки обязателен')
            return redirect('loadFiles:upload')
            
        try:
            student = Student.objects.get(record_book__iexact=record_book)
            category = request.POST.get('category')
            score = int(request.POST.get('score', 0))
            files = request.FILES.getlist('files')
            
            if not category:
                messages.error(request, 'Не выбрана категория достижения')
                return redirect('loadFiles:upload')
                
            if score <= 0:
                messages.error(request, 'Количество баллов должно быть положительным')
                return redirect('loadFiles:upload')
            
            achievement = Document.objects.create(
                student=student,
                category=category,
                achievement=request.POST.get('achievement', ''),
                score=score,
                doc_type=request.POST.get('doc_type', 'other')
            )
            

            if files:
                achievement.file = files[0]
                achievement.save()
                
                for file in files[1:]:
                    Document.objects.create(
                        student=student,
                        category=category,
                        achievement=request.POST.get('achievement', ''),
                        score=score,
                        doc_type=request.POST.get('doc_type', 'other'),
                        file=file
                    )
            
            total_score = score * (len(files) if files else 1)
            Student.objects.filter(pk=student.pk).update(
                **{f'{category}_score': F(f'{category}_score') + total_score}
            )
            
            messages.success(request, 'Достижение успешно добавлено!')
            return redirect('loadFiles:upload')
            
        except Student.DoesNotExist:
            messages.error(request, f'Студент с номером "{record_book}" не найден')
        except ValueError:
            messages.error(request, 'Некорректное значение баллов')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
    
    return render(request, 'loadFiles/index.html')