"""
Tests pour les endpoints des catégories
"""
import pytest
from fastapi import status

def test_get_categories_empty(client):
    """Test GET /categories avec base vide"""
    response = client.get("/api/v1/categories/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_categories_with_data(client, sample_category):
    """Test GET /categories avec données"""
    response = client.get("/api/v1/categories/")
    assert response.status_code == status.HTTP_200_OK
    
    categories = response.json()
    assert len(categories) == 1
    assert categories[0]["name"] == "Test Category"
    assert categories[0]["tasks_count"] == 0

def test_create_category_success(client):
    """Test POST /categories avec données valides"""
    category_data = {
        "name": "Nouvelle Catégorie",
        "description": "Description de test",
        "color": "#28a745"
    }
    
    response = client.post("/api/v1/categories/", json=category_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    created_category = response.json()
    assert created_category["name"] == "Nouvelle Catégorie"
    assert created_category["description"] == "Description de test"
    assert created_category["color"] == "#28a745"
    assert "id" in created_category

def test_create_category_validation_error(client):
    """Test POST /categories avec données invalides"""
    # Nom trop court
    response = client.post("/api/v1/categories/", json={"name": ""})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_category_duplicate_name(client, sample_category):
    """Test POST /categories avec nom déjà existant"""
    category_data = {
        "name": "Test Category",  # Nom déjà existant
        "description": "Autre description"
    }
    
    response = client.post("/api/v1/categories/", json=category_data)
    assert response.status_code == status.HTTP_409_CONFLICT

def test_get_category_by_id(client, sample_category):
    """Test GET /categories/{id}"""
    response = client.get(f"/api/v1/categories/{sample_category.id}")
    assert response.status_code == status.HTTP_200_OK
    
    category = response.json()
    assert category["id"] == sample_category.id
    assert category["name"] == sample_category.name

def test_get_category_not_found(client):
    """Test GET /categories/{id} avec ID inexistant"""
    response = client.get("/api/v1/categories/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_category(client, sample_category):
    """Test PUT /categories/{id}"""
    update_data = {
        "name": "Catégorie Modifiée",
        "description": "Description modifiée"
    }
    
    response = client.put(f"/api/v1/categories/{sample_category.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    
    updated_category = response.json()
    assert updated_category["name"] == "Catégorie Modifiée"
    assert updated_category["description"] == "Description modifiée"

def test_delete_category_success(client, sample_category):
    """Test DELETE /categories/{id} sans tâches"""
    response = client.delete(f"/api/v1/categories/{sample_category.id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Vérifier que la catégorie n'existe plus
    get_response = client.get(f"/api/v1/categories/{sample_category.id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_category_with_tasks(client, sample_task):
    """Test DELETE /categories/{id} avec tâches associées"""
    response = client.delete(f"/api/v1/categories/{sample_task.category_id}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY