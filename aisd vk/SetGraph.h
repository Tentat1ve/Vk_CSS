#pragma once
#include "IGraph.h"

struct Node {
    int value;
    Node* next;
    Node(int val) : value(val), next(nullptr) {}
};

class SetGraph : public IGraph {
public:
    explicit SetGraph(int verticesCount);
    explicit SetGraph(const IGraph& graph);
    ~SetGraph();
    
    void AddEdge(int from, int to) override;
    int VerticesCount() const override;
    int* GetNextVertices(int vertex, int& count) const override;
    int* GetPrevVertices(int vertex, int& count) const override;

private:
    int verticesCount;
    Node** adjacencySets;
    
    bool contains(Node* list, int value) const;
    void insert(Node*& list, int value);
    void clearList(Node* list);
    int listSize(Node* list) const;
    int* listToArray(Node* list, int& size) const;
};