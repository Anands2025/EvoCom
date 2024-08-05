from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Community, UserCommunity

@login_required
def create_community(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        cover= request.FILES.get('cover')
        community = Community(
            name=name,
            description=description,
            created_by=request.user,
            admin=request.user,
            cover=cover
            )
        community.save()
        return redirect('users:community_admin_index')
    return render(request, 'communities/create_community.html')
@login_required
def update_community(request):
    user=request.user
    community = Community.objects.get(admin=user)
    if request.method == 'POST':
        name = request.POST.get('community_name')
        description = request.POST.get('community_description')
        cover= request.FILES.get('cover_image')
        community.name=name
        community.description=description
        community.cover=cover
        community.save()
        return redirect('communities:community_management')

@login_required
def community_management(request):
    user=request.user
    community = Community.objects.get(admin=user)
    return render(request, 'communities/community_management.html', {'community': community})

@login_required
def show_communities(request):
    communities = Community.objects.all()
    return render(request, 'communities/show_communities.html', {'communities': communities})
@login_required
def view_community(request, pk):
    community = get_object_or_404(Community, pk=pk)   
    if request.method == 'POST':
        UserCommunity.objects.create(user=request.user, community=community)
        messages.success(request, 'You have joined the community!')
        return redirect('view_community', pk=community.pk)

    return render(request, 'communities/view_community.html', {'community': community})
@login_required
def view_community(request, pk):
    community = get_object_or_404(Community, pk=pk)   
    is_member = UserCommunity.objects.filter(user=request.user, community=community).exists()
    context = {
        'community': community,
        'is_member': is_member,
    }
    return render(request, 'communities/view_community.html', context)

@login_required
def join_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    UserCommunity.objects.get_or_create(user=request.user, community=community)
    return redirect('communities:view_community', pk=community.id)

@login_required
def joined_communities(request):
    user = request.user
    communities = Community.objects.filter(usercommunity__user=user)
    return render(request, 'communities/joined_communities.html', {'communities': communities})