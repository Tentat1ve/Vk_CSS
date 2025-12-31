#include "SetGraph.h"

SetGraph::SetGraph(int verticesCount) : verticesCount(verticesCount) {
    adjacencySets = new Node*[verticesCount];
    for (int i = 0; i < verticesCount; ++i) {
        adjacencySets[i] = nullptr;
    }
}

SetGraph::SetGraph(const IGraph& graph) : verticesCount(graph.VerticesCount()) {
    adjacencySets = new Node*[verticesCount];
    for (int i = 0; i < verticesCount; ++i) {
        adjacencySets[i] = nullptr;
    }
    
    for (int i = 0; i < verticesCount; ++i) {
        int count = 0;
        int* next = graph.GetNextVertices(i, count);
        for (int j = 0; j < count; ++j) {
            AddEdge(i, next[j]);
        }
        delete[] next;
    }
}

SetGraph::~SetGraph() {
    for (int i = 0; i < verticesCount; ++i) {
        clearList(adjacencySets[i]);
    }
    delete[] adjacencySets;
}

bool SetGraph::contains(Node* list, int value) const {
    Node* current = list;
    while (current) {
        if (current->value == value) return true;
        current = current->next;
    }
    return false;
}

void SetGraph::insert(Node*& list, int value) {
    if (!contains(list, value)) {
        Node* newNode = new Node(value);
        newNode->next = list;
        list = newNode;
    }
}

void SetGraph::clearList(Node* list) {
    while (list) {
        Node* temp = list;
        list = list->next;
        delete temp;
    }
}

int SetGraph::listSize(Node* list) const {
    int size = 0;
    while (list) {
        size++;
        list = list->next;
    }
    return size;
}

int* SetGraph::listToArray(Node* list, int& size) const {
    size = listSize(list);
    if (size == 0) return nullptr;
    
    int* arr = new int[size];
    for (int i = 0; i < size; ++i) {
        arr[i] = list->value;
        list = list->next;
    }
    return arr;
}

void SetGraph::AddEdge(int from, int to) {
    if (from >= 0 && from < verticesCount && to >= 0 && to < verticesCount) {
        insert(adjacencySets[from], to);
    }
}

int SetGraph::VerticesCount() const {
    return verticesCount;
}

int* SetGraph::GetNextVertices(int vertex, int& count) const {
    if (vertex >= 0 && vertex < verticesCount) {
        return listToArray(adjacencySets[vertex], count);
    }
    count = 0;
    return nullptr;
}

int* SetGraph::GetPrevVertices(int vertex, int& count) const {
    if (vertex >= 0 && vertex < verticesCount) {
        int* temp = new int[verticesCount];
        count = 0;
        
        for (int i = 0; i < verticesCount; ++i) {
            if (contains(adjacencySets[i], vertex)) {
                temp[count++] = i;
            }
        }
        
        int* result = new int[count];
        for (int i = 0; i < count; ++i) {
            result[i] = temp[i];
        }
        delete[] temp;
        return result;
    }
    count = 0;
    return nullptr;
}