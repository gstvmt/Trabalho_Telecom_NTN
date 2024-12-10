import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
  
class ImageSubscriber(Node):
  
  def __init__(self):
    """
    Inicializa a classe ImageSubscriber.
    
    Configura o nó do ROS, cria a assinatura do tópico 'jetson_webcam', 
    e define a função de callback 'listener_callback' para receber e processar 
    mensagens de imagem. Também cria a instância de CvBridge para conversão 
    entre ROS e OpenCV.
    """

    super().__init__('image_subscriber')
    self.subscription = self.create_subscription(
      Image, 
      'jetson_webcam', 
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning
    self.br = CvBridge()
    
  def listener_callback(self, data):
    """
    Função de callback chamada quando uma mensagem de imagem é recebida.
    
    Recebe uma mensagem do tipo Image, converte para um quadro OpenCV e exibe
    o vídeo em uma janela chamada "camera". A janela é atualizada com cada novo quadro
    recebido.
    
    Parâmetros:
    - data: Mensagem recebida, do tipo Image, contendo o quadro de vídeo.
    """
    
    self.get_logger().info('Receiving video frame')
    current_frame = self.br.imgmsg_to_cv2(data)
    cv2.imshow("camera", current_frame)
    cv2.waitKey(1)
   
def main(args=None):
  rclpy.init(args=args)
  image_subscriber = ImageSubscriber()
  rclpy.spin(image_subscriber)
  image_subscriber.destroy_node()
  rclpy.shutdown()
   
if __name__ == '__main__':
  main()