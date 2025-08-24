from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save  #usara signals
from django.dispatch import receiver  #para recibir los sginals

#CURSOS
class Course(models.Model):
    name= models.CharField(max_length=90, verbose_name='Nombre')
    description =models.TextField(blank=True, null=True, verbose_name='Description')
    teacher= models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'profesores'}, verbose_name='Profesor')
    class_quantity= models.PositiveIntegerField(default=0,verbose_name='Cantidad de clases')
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name ='Curso'
        verbose_name_plural= 'Cursos'
        
#INSCRIPCIONES
class Registration(models.Model):
    course= models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    student= models.ForeignKey(User, on_delete=models.CASCADE, related_name='students_registration', limit_choices_to={'groups__name':'estudiantes'},verbose_name='Estudiante')
    enabled = models.BooleanField(default=True, verbose_name='Alumno regular')
    def __str__(self):
        return f'{self.student.username} - { self.course.name}'
    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        
#ASISTENCIAS
class Attendance(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    student=models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances', limit_choices_to={'groups__name': 'estudiantes'}, verbose_name='Estudiante') 
    date = models.DateField (null=True, blank=True, verbose_name='Fecha')
    present= models.BooleanField(default=False, blank=True, null=True, verbose_name='Presente') 
    
    def __str__(self):
        return f'Asistencia {self.id}'
    
    #lógica para asignar estudiante True o False segun su porcentaje de asistencias.
    def update_registration_enable_status(self):
        #Instancias de otros modelos
        course_instance = Course.objects.get(id=self.course.id) #intancia course
        total_absences = Attendance.objects.filter(student=self.student, course=self.course, present=False).count() #intancia attendance
        registration= Registration.objects.get(course=self.course, student=self.student)
        
        total_classes = course_instance.class_quantity  # class_quantity = variable con cantidad de clases int.
        absence_percent= (total_absences / total_classes ) * 100
        
        if absence_percent > 20:
            registration.enabled =False
        else: 
            registration.enabled = True
        
        registration.save()
        
      
    class Meta:  
        verbose_name ='Asistencia'
        verbose_name_plural = 'Asistencias'
        
        
       
    
#NOTAS    
class Mark(models.Model):
    
    course=models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    student=models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'estudiantes'}, verbose_name='Estudiante') 
    mark_1=models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 1')
    mark_2=models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 2')
    mark_3=models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 3')
    average = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name='promedio')
    
    def calculate_average(self):
        marks = [self.mark_1, self.mark_2, self.mark_3] # crearr array con la info
        valid_marks = [mark for mark in marks if mark is not None] # iterar la array y validar, solo trae los no null
        if valid_marks:
            return sum(valid_marks)/ len(valid_marks) # promedio
        return None
        
    def save(self, *args, **kwargs):
        #verifico si alguna nota cambio
        if self.mark_1 or self.mark_2 or self.mark_3:
            self.average = self.calculate_average()  #calcular el promedio, (llamo la funcion)
        super().save(*args, **kwargs)
            
    class Meta:
        verbose_name='Nota'
        verbose_name_plural='Notas'


@receiver(post_save, sender=Attendance)  #reciver =rrecpector  sender=remitente
@receiver(post_delete, sender=Attendance)
def update_registration_enable_status(sender, instance, **kwargs):
    instance.update_registration_enable_status()  #llamo a la funcion creada anteriormente

            