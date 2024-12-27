import grpc
import book_pb2
import book_pb2_grpc

def check_book_availability(book_id):
    channel = grpc.insecure_channel('grpc-service.default.svc.cluster.local:50051')

    stub = book_pb2_grpc.BookServiceStub(channel)
    request = book_pb2.BookRequest(book_id=book_id)

    try:
        # Call the GetBook method
        response = stub.GetBook(request)
        print("Book retrieved successfully: ")
        print(f"ID: {response.id}, Title: {response.title}, Author: {response.author}, Year: {response.year}")
        return response.stock > 0
    except grpc.RpcError as e:
        print(f"Failed to get book: {e}")

    return False

