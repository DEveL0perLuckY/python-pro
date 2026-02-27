from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import AppUser


@csrf_exempt
def user_list_create(request):
    if request.method == "GET":
        # Read (List) all users from the database
        users = list(AppUser.objects.values('id', 'name', 'email'))
        return JsonResponse({"users": users}, status=200)
    
    elif request.method == "POST":
        # Create a new user in the database
        try:
            data = json.loads(request.body)
            # Create user in db.sqlite3
            new_user = AppUser.objects.create(
                name=data.get("name", ""),
                email=data.get("email", "")
            )
            return JsonResponse({
                "message": "User created successfully", 
                "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email}
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            # e.g., IntegrityError for duplicate email
            return JsonResponse({"error": str(e)}, status=400)
            
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def user_detail_update_delete(request, user_id):
    try:
        user = AppUser.objects.get(id=user_id)
    except AppUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
        
    if request.method == "GET":
        # Read a specific user from the database
        return JsonResponse({"user": {"id": user.id, "name": user.name, "email": user.email}}, status=200)
        
    elif request.method == "PUT":
        # Update a specific user in the database
        try:
            data = json.loads(request.body)
            user.name = data.get("name", user.name)
            user.email = data.get("email", user.email)
            user.save()  # Saves changes to db.sqlite3
            return JsonResponse({
                "message": "User updated successfully", 
                "user": {"id": user.id, "name": user.name, "email": user.email}
            }, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
            
    elif request.method == "DELETE":
        # Delete a specific user from the database
        user.delete()
        return JsonResponse({"message": "User deleted successfully"}, status=200)
        
    return JsonResponse({"error": "Method not allowed"}, status=405)
