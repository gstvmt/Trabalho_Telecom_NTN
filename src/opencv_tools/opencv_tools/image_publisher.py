import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
  
class ImagePublisher(Node):
  
  def __init__(self):
    """
    Inicializa a classe ImagePublisher.
    
    Configura o nó do ROS, cria o publicador de imagens e o temporizador,
    e inicializa a captura de vídeo da câmera padrão (índice 0).
    Também cria a instância de CvBridge para conversão entre OpenCV e ROS.
    """

    super().__init__('image_publisher')
    self.publisher_ = self.create_publisher(Image, 'jetson_webcam', 10)
    timer_period = 0.1
    self.timer = self.create_timer(timer_period, self.timer_callback)
    self.cap = cv2.VideoCapture(0)
    self.br = CvBridge()
    
  def timer_callback(self):
    """
    Função de callback chamada periodicamente pelo temporizador.
    
    Captura um quadro de vídeo da câmera e publica no tópico 'jetson_webcam'.
    Caso a captura seja bem-sucedida, converte o quadro para uma mensagem do tipo 
    Image e o publica no tópico usando o publicador.
    """

    ret, frame = self.cap.read()
    if ret == True:
      self.publisher_.publish(self.br.cv2_to_imgmsg(frame))
    self.get_logger().info('Publishing video frame')
   
def main(args=None):
  """
  Função principal que inicia o nó ROS e mantém o nó ativo.
  
  Inicia o sistema ROS, cria uma instância de ImagePublisher e mantém o nó
  ativo processando callbacks. Após a execução, o nó é destruído e o sistema ROS é desligado.
  """
  
  rclpy.init(args=args)
  image_publisher = ImagePublisher()
  rclpy.spin(image_publisher)
  image_publisher.destroy_node()
  rclpy.shutdown()
   
if __name__ == '__main__':
  main()