#include "ListGraph.h"
#include <algorithm>

ListGraph::ListGraph(int verticesCount) : verticesCount(verticesCount) {
    adjacencyLists = new int*[verticesCount];
    listSizes = new int[verticesCount];
    for (int i = 0; i < verticesCount; ++i) {
        adjacencyLists[i] = nullptr;
        listSizes[i] = 0;
    }
}

ListGraph::ListGraph(const IGraph& graph) : verticesCount(graph.VerticesCount()) {
    adjacencyLists = new int*[verticesCount];
    listSizes = new int[verticesCount];
    
    for (int i = 0; i < verticesCount; ++i) {
        int count = 0;
        int* nextVertices = graph.GetNextVertices(i, count);
        adjacencyLists[i] = new int[count];
        listSizes[i] = count;
        for (int j = 0; j < count; ++j) {
            adjacencyLists[i][j] = nextVertices[j];
        }
        delete[] nextVertices;
    }
}

ListGraph::~ListGraph() {
    for (int i = 0; i < verticesCount; ++i) {
        delete[] adjacencyLists[i];
    }
    delete[] adjacencyLists;
    delete[] listSizes;
}

void ListGraph::AddEdge(int from, int to) {
    if (from >= 0 && from < verticesCount && to >= 0 && to < verticesCount) {
        int* newList = new int[listSizes[from] + 1];
        for (int i = 0; i < listSizes[from]; ++i) {
            newList[i] = adjacencyLists[from][i];
        }
        newList[listSizes[from]] = to;
        delete[] adjacencyLists[from];
        adjacencyLists[from] = newList;
        listSizes[from]++;
    }
}

int ListGraph::VerticesCount() const {
    return verticesCount;
}

int* ListGraph::GetNextVertices(int vertex, int& count) const {
    if (vertex >= 0 && vertex < verticesCount) {
        count = listSizes[vertex];
        int* result = new int[count];
        for (int i = 0; i < count; ++i) {
            result[i] = adjacencyLists[vertex][i];
        }
        return result;
    }
    count = 0;
    return nullptr;
}

int* ListGraph::GetPrevVertices(int vertex, int& count) const {
    if (vertex >= 0 && vertex < verticesCount) {
        int* temp = new int[verticesCount];
        count = 0;
        
        for (int from = 0; from < verticesCount; ++from) {
            for (int j = 0; j < listSizes[from]; ++j) {
                if (adjacencyLists[from][j] == vertex) {
                    temp[count++] = from;
                    break;
                }
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