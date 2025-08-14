"""
Tests pour les endpoints des tâches
"""
import pytest
from fastapi import status
from datetime import datetime, timedelta

def test_get_tasks_empty(client):
    """Test GET /tasks avec base vide"""
    response = client.get("/api/v1/tasks/")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0

def test_get_tasks_with_data(client, sample_task):
    """Test GET /tasks avec données"""
    response = client.get("/api/v1/tasks/")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Tâche de test"

def test_create_task_success(client, sample_category):
    """Test POST /tasks avec données valides"""
    task_data = {
        "title": "Nouvelle tâche de test",
        "description": "Description détaillée",
        "priority": "Haute",
        "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
        "category_id": sample_category.id
    }
    
    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    created_task = response.json()
    assert created_task["title"] == "Nouvelle tâche de test"
    assert created_task["priority"] == "Haute"
    assert created_task["category"]["id"] == sample_category.id

def test_create_task_validation_errors(client, sample_category):
    """Test POST /tasks avec données invalides"""
    # Titre trop court
    response = client.post("/api/v1/tasks/", json={
        "title": "AB",  # Moins de 3 caractères
        "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "category_id": sample_category.id
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Date dans le passé
    response = client.post("/api/v1/tasks/", json={
        "title": "Tâche valide",
        "due_date": (datetime.now() - timedelta(days=1)).isoformat(),
        "category_id": sample_category.id
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_task_by_id(client, sample_task):
    """Test GET /tasks/{id}"""
    response = client.get(f"/api/v1/tasks/{sample_task.id}")
    assert response.status_code == status.HTTP_200_OK
    
    task = response.json()
    assert task["id"] == sample_task.id
    assert task["title"] == sample_task.title

def test_update_task(client, sample_task):
    """Test PUT /tasks/{id}"""
    update_data = {
        "title": "Tâche modifiée",
        "priority": "Haute",
        "status": "Terminée"
    }
    
    response = client.put(f"/api/v1/tasks/{sample_task.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    
    updated_task = response.json()
    assert updated_task["title"] == "Tâche modifiée"
    assert updated_task["priority"] == "Haute"
    assert updated_task["status"] == "Terminée"
    assert updated_task["completed_at"] is not None

def test_delete_task(client, sample_task):
    """Test DELETE /tasks/{id}"""
    response = client.delete(f"/api/v1/tasks/{sample_task.id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Vérifier que la tâche n'existe plus
    get_response = client.get(f"/api/v1/tasks/{sample_task.id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_complete_task(client, sample_task):
    """Test PATCH /tasks/{id}/complete"""
    response = client.patch(f"/api/v1/tasks/{sample_task.id}/complete")
    assert response.status_code == status.HTTP_200_OK
    
    completed_task = response.json()
    assert completed_task["status"] == "Terminée"
    assert completed_task["completed_at"] is not None

def test_search_tasks(client, sample_task):
    """Test GET /tasks/search/"""
    response = client.get("/api/v1/tasks/search/?q=test")
    assert response.status_code == status.HTTP_200_OK
    
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Tâche de test"

def test_get_urgent_tasks(client):
    """Test GET /tasks/urgent/list"""
    response = client.get("/api/v1/tasks/urgent/list")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_get_statistics(client, sample_task):
    """Test GET /tasks/statistics/"""
    response = client.get("/api/v1/tasks/statistics/")
    assert response.status_code == status.HTTP_200_OK
    
    stats = response.json()
    assert "total" in stats
    assert "by_status" in stats
    assert "by_priority" in stats
    assert stats["total"] == 1