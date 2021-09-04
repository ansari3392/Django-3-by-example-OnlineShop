from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.contrib import messages


from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


class Register(CreateView):

    def post(self, *args, **kwargs):
        user_form = UserRegistrationForm(self.request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(self.request, 'account/register_done.html', {'new_user': new_user})
            
    def get(self, *args, **kwargs):   
        user_form = UserRegistrationForm(self.request.POST)
        return render(self.request, 'account/register.html', {'user_form': user_form})



class EditView(UpdateView):
    def post(self, *args, **kwargs):
        user_form = UserEditForm(instance=self.request.user, data=self.request.POST)
        profile_form = ProfileEditForm(instance=self.request.user.profile, data=self.request.POST, files=self.request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(self.request, 'Profile updated successfully')
        else:
            messages.error(self.request, 'Error updating your profile')

        return render(self.request, 'account/edit.html',{'user_form': user_form,'profile_form': profile_form})
    

    def get(self, *args, **kwargs):   
        user_form = UserEditForm(instance=self.request.user) 
        profile_form = ProfileEditForm(instance=self.request.user.profile)
        return render(self.request,'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
            