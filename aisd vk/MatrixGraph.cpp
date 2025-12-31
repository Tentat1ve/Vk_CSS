#include "MatrixGraph.h"

MatrixGraph::MatrixGraph(int verticesCount) : verticesCount(verticesCount) {
    matrix = new bool*[verticesCount];
    for (int i = 0; i < verticesCount; ++i) {
        matrix[i] = new bool[verticesCount];
        for (int j = 0; j < verticesCount; ++j) {
            matrix[i][j] = false;
        }
    }
}

MatrixGraph::MatrixGraph(const IGraph& graph) : verticesCount(graph.VerticesCount()) {
    matrix = new bool*[verticesCount];
    for (int i = 0; i < verticesCount; ++i) {
        matrix[i] = new bool[verticesCount];
        for (int j = 0; j < verticesCount; ++j) {
            matrix[i][j] = false;
        }
    }
    
    for (int i = 0; i < verticesCount; ++i) {
        int count = 0;
        int* next = graph.GetNextVertices(i, count);
        for (int j = 0; j < count; ++j) {
            matrix[i][next[j]] = true;
        }
        delete[] next;
    }
}

MatrixGraph::~MatrixGraph() {
    for (int i = 0; i < verticesCount; ++i) {
        delete[] matrix[i];
    }
    delete[] matrix;
}

void MatrixGraph::AddEdge(int from, int to) {
    if (from >= 0 && from < verticesCount && to >= 0 && to < verticesCount) {
        matrix[from][to] = true;
    }
}

int MatrixGraph::VerticesCount() const {
    return verticesCount;
}

int* MatrixGraph::GetNextVertices(int vertex, int& count) const {
    if (vertex >= 0 && vertex < verticesCount) {
        int* temp = new int[verticesCount];
        count = 0;
        
        for (int i = 0; i < verticesCount; ++i) {
            if (matrix[vertex][i]) {
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

int* MatrixGraph::GetPrevVertices(int vertex, int& count) const {
    if (vertex >= 0 && vertex < verticesCount) {
        int* temp = new int[verticesCount];
        count = 0;
        
        for (int i = 0; i < verticesCount; ++i) {
            if (matrix[i][vertex]) {
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