#include "ArcGraph.h"

ArcGraph::ArcGraph(int verticesCount) : verticesCount(verticesCount), edges(nullptr) {}

ArcGraph::ArcGraph(const IGraph& graph) : verticesCount(graph.VerticesCount()), edges(nullptr) {
    for (int i = 0; i < verticesCount; ++i) {
        int count = 0;
        int* next = graph.GetNextVertices(i, count);
        for (int j = 0; j < count; ++j) {
            AddEdge(i, next[j]);
        }
        delete[] next;
    }
}

ArcGraph::~ArcGraph() {
    Edge* current = edges;
    while (current) {
        Edge* next = current->next;
        delete current;
        current = next;
    }
}

void ArcGraph::AddEdge(int from, int to) {
    if (from >= 0 && from < verticesCount && to >= 0 && to < verticesCount) {
        Edge* newEdge = new Edge(from, to);
        newEdge->next = edges;
        edges = newEdge;
    }
}

int ArcGraph::VerticesCount() const {
    return verticesCount;
}

int* ArcGraph::GetNextVertices(int vertex, int& count) const {
    if (vertex >= 0 && vertex < verticesCount) {
        int* temp = new int[verticesCount];
        count = 0;
        
        Edge* current = edges;
        while (current) {
            if (current->from == vertex) {
                temp[count++] = current->to;
            }
            current = current->next;
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

int* ArcGraph::GetPrevVertices(int vertex, int& count) const {
    if (vertex >= 0 && vertex < verticesCount) {
        int* temp = new int[verticesCount];
        count = 0;
        
        Edge* current = edges;
        while (current) {
            if (current->to == vertex) {
                temp[count++] = current->from;
            }
            current = current->next;
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