import numpy
import os
import time
import pygadgetron

class error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def _check_status(handle):
    if pygadgetron.executionStatus(handle) != 0:
        msg = pygadgetron.executionError(handle)
        file = pygadgetron.executionErrorFile(handle)
        line = pygadgetron.executionErrorLine(handle)
        errorMsg = \
            repr(msg) + ' exception thrown at line ' + \
            repr(line) + ' of ' + file
        raise error(errorMsg)

def _int_par(handle, set, par):
    h = pygadgetron.cGT_parameter(handle, set, par)
    _check_status(h)
    value = pygadgetron.intDataFromHandle(h)
    pygadgetron.deleteDataHandle(h)
    return value

class PyGadgetronObject:
    pass
	
class ClientConnector(PyGadgetronObject):
    def __init__(self):
        self.handle = None
        self.handle = pygadgetron.cGT_newObject('GTConnector')
        _check_status(self.handle)
    def __del__(self):
        if self.handle is not None:
            pygadgetron.deleteObject(self.handle)
    def set_timeout(self, timeout):
        handle = pygadgetron.cGT_setConnectionTimeout(self.handle, timeout)
        _check_status(handle)
        pygadgetron.deleteDataHandle(handle)
    def connect(self, host, port):
        handle = pygadgetron.cGT_connect(self.handle, host, port)
        _check_status(handle)
        pygadgetron.deleteDataHandle(handle)
    def disconnect(self):
        handle = pygadgetron.cGT_disconnect(self.handle)
        _check_status(handle)
        pygadgetron.deleteDataHandle(handle)
    def register_HDF_receiver(self, file, group):
        handle = pygadgetron.cGT_registerHDFReceiver(self.handle, file, group)
        _check_status(handle)
        pygadgetron.deleteDataHandle(handle)
    def register_images_receiver(self, imgs):
        handle = pygadgetron.cGT_registerImagesReceiver\
            (self.handle, imgs.handle)
        _check_status(handle)
        pygadgetron.deleteDataHandle(handle)
    def config_gadget_chain(self, gc):
        handle = pygadgetron.cGT_configGadgetChain(self.handle, gc.handle)
        _check_status(handle)
        pygadgetron.deleteDataHandle(handle)
    def send_config_file(self, file):
        handle = pygadgetron.cGT_sendConfigFile(self.handle, file)
        _check_status(handle)
        pygadgetron.deleteDataHandle(handle)
    def send_parameters(self, par):
        handle = pygadgetron.cGT_sendParameters(self.handle, par)
        _check_status(handle)
        pygadgetron.deleteDataHandle(handle)
    def send_acquisitions(self, acq):
        handle = pygadgetron.cGT_sendAcquisitions(self.handle, acq.handle)
        _check_status(handle)
        pygadgetron.deleteDataHandle(handle)
    def send_images(self, img):
        handle = pygadgetron.cGT_sendImages(self.handle, img.handle)
        _check_status(handle)
        pygadgetron.deleteDataHandle(handle)
        
class ImagesContainer(PyGadgetronObject):
    def __init__(self):
        self.handle = None
    def __del__(self):
        if self.handle is not None:
            pygadgetron.deleteObject(self.handle)
    def number(self):
        return pygadgetron.cGT_numImages(self.handle)
    def norm(self):
        handle = pygadgetron.cGT_norm(self.handle)
        _check_status(handle)
        r = pygadgetron.doubleDataFromHandle(handle)
        pygadgetron.deleteDataHandle(handle)
        return r;
    def dot(self, images):
        handle = pygadgetron.cGT_dot(self.handle, images.handle)
        _check_status(handle)
        re = pygadgetron.doubleReDataFromHandle(handle)
        im = pygadgetron.doubleImDataFromHandle(handle)
        pygadgetron.deleteDataHandle(handle)
        return complex(re, im)
    @staticmethod
    def axpby(a, x, b, y):
        z = ImagesContainer()
##        z.handle = pygadgetron.cGT_imagesZaxpby\
        z.handle = pygadgetron.cGT_axpby\
            (a.real, a.imag, x.handle, b.real, b.imag, y.handle)
        return z;
    def write(self, out_file, out_group):
        handle = pygadgetron.cGT_writeImages\
            (self.handle, out_file, out_group)
        _check_status(handle)
        pygadgetron.deleteDataHandle(handle)
    def image_as_array(self, im_num):
        dim = numpy.ndarray((4,), dtype = numpy.int32)
        pygadgetron.cGT_getImageDimensions\
            (self.handle, im_num, dim.ctypes.data)
        nx = dim[0]
        ny = dim[1]
        nz = dim[2]
        nc = dim[3]
        if nx == 0 or ny == 0 or nz == 0 or nc == 0:
            raise error('image data not available')
##        array = numpy.ndarray((nx, ny, nz, nc), dtype = numpy.float64)
        array = numpy.ndarray((nc, nz, ny, nx), dtype = numpy.float64)
        pygadgetron.cGT_getImageDataAsDoubleArray\
            (self.handle, im_num, array.ctypes.data)
        return array
    def image_as_complex_array(self, im_num):
        dim = numpy.ndarray((4,), dtype = numpy.int32)
        pygadgetron.cGT_getImageDimensions\
            (self.handle, im_num, dim.ctypes.data)
        nx = dim[0]
        ny = dim[1]
        nz = dim[2]
        nc = dim[3]
        if nx == 0 or ny == 0 or nz == 0 or nc == 0:
            raise error('image data not available')
        array = numpy.ndarray((nc, nz, ny, nx), dtype = numpy.complex64)
        pygadgetron.cGT_getImageDataAsComplexArray\
            (self.handle, im_num, array.ctypes.data)
        return array

class AcquisitionsContainer(PyGadgetronObject):
    def __init__(self):
        self.handle = None
    def __del__(self):
        if self.handle is not None:
            pygadgetron.deleteObject(self.handle)
    def norm(self):
        handle = pygadgetron.cGT_norm(self.handle)
        _check_status(handle)
        r = pygadgetron.doubleDataFromHandle(handle)
        pygadgetron.deleteDataHandle(handle)
        return r;
    def dot(self, acqs):
        handle = pygadgetron.cGT_dot(self.handle, acqs.handle)
        _check_status(handle)
        re = pygadgetron.doubleReDataFromHandle(handle)
        im = pygadgetron.doubleImDataFromHandle(handle)
        pygadgetron.deleteDataHandle(handle)
        return complex(re, im)
    @staticmethod
    def axpby(a, x, b, y):
        z = AcquisitionsContainer()
##        z.handle = pygadgetron.cGT_acquisitionsZaxpby\
        z.handle = pygadgetron.cGT_axpby\
            (a.real, a.imag, x.handle, b.real, b.imag, y.handle)
        return z;

class ISMRMRDAcquisition(PyGadgetronObject):
    def __init__(self, file = None):
        self.handle = None
    def __del__(self):
        if self.handle is not None:
            pygadgetron.deleteObject(self.handle)
    def flags(self):
        return _int_par(self.handle, 'acquisition', 'flags')
    def number_of_samples(self):
        return _int_par(self.handle, 'acquisition', 'number_of_samples')
    def active_channels(self):
        return _int_par(self.handle, 'acquisition', 'active_channels')
    def trajectory_dimensions(self):
        return _int_par(self.handle, 'acquisition', 'trajectory_dimensions')
    def idx_kspace_encode_step_1(self):
        return _int_par(self.handle, 'acquisition', 'idx_kspace_encode_step_1')
    def idx_repetition(self):
        return _int_par(self.handle, 'acquisition', 'idx_repetition')
    def idx_slice(self):
        return _int_par(self.handle, 'acquisition', 'idx_slice')

class ISMRMRDAcquisitions(AcquisitionsContainer):
    def __init__(self, file = None):
        self.handle = None
        if file is not None:
            self.handle = pygadgetron.cGT_ISMRMRDAcquisitionsFromFile(file)
            _check_status(self.handle)
    def __del__(self):
        if self.handle is not None:
            pygadgetron.deleteObject(self.handle)
    def acquisition(self, num):
        acq = ISMRMRDAcquisition()
        acq.handle = pygadgetron.cGT_acquisitionFromContainer(self.handle, num)
        return acq

class AcquisitionModel(PyGadgetronObject):
    def __init__(self, acqs, imgs):
        self.handle = None
        self.handle = \
            pygadgetron.cGT_AcquisitionModel(acqs.handle, imgs.handle)
        _check_status(self.handle)
        self.images = imgs
    def __del__(self):
        if self.handle is not None:
            pygadgetron.deleteObject(self.handle)
    def forward(self, images):
        acqs = ISMRMRDAcquisitions()
        acqs.handle = pygadgetron.cGT_AcquisitionModelForward\
            (self.handle, images.handle)
        _check_status(acqs.handle)
        return acqs;
    def backward(self, acqs):
        images = ImagesContainer()
        images.handle = pygadgetron.cGT_AcquisitionModelBackward\
            (self.handle, acqs.handle)
        _check_status(images.handle)
        return images

class GadgetChain(PyGadgetronObject):
    def __init__(self):
        self.handle = pygadgetron.cGT_newObject('GadgetChain')
        _check_status(self.handle)
    def __del__(self):
        if self.handle is not None:
            pygadgetron.deleteObject(self.handle)
    def add_reader(self, id, reader):
        handle = pygadgetron.cGT_addReader(self.handle, id, reader.handle)
        _check_status(handle)
        pygadgetron.deleteDataHandle(handle)
    def add_writer(self, id, writer):
        handle = pygadgetron.cGT_addWriter(self.handle, id, writer.handle)
        _check_status(handle)
        pygadgetron.deleteDataHandle(handle)
    def add_gadget(self, id, gadget):
        handle = pygadgetron.cGT_addGadget(self.handle, id, gadget.handle)
        _check_status(handle)
        pygadgetron.deleteDataHandle(handle)

class ImagesReconstructor(GadgetChain):
    def __init__(self):
        self.handle = None
        self.handle = pygadgetron.cGT_newObject('ImagesReconstructor')
        _check_status(self.handle)
        self.input_data = None
    def __del__(self):
        if self.handle is not None:
            #print('deleting reconstructor object...')
            pygadgetron.deleteObject(self.handle)
    def set_input(self, input_data):
        self.input_data = input_data
    def process(self):
        if self.input_data is None:
            raise error('no input data')
        handle = pygadgetron.cGT_reconstructImages\
             (self.handle, self.input_data.handle)
        _check_status(handle)
        pygadgetron.deleteDataHandle(handle)
    def get_output(self):
        images = ImagesContainer()
        images.handle = pygadgetron.cGT_reconstructedImages(self.handle)
        _check_status(images.handle)
        return images

class ImagesProcessor(GadgetChain):
    def __init__(self):
        self.handle = None
        self.handle = pygadgetron.cGT_newObject('ImagesProcessor')
        _check_status(self.handle)
        self.input_data = None
    def __del__(self):
        if self.handle is not None:
            pygadgetron.deleteObject(self.handle)
##    def set_input(self, input_data):
##        self.input_data = input_data
    def process(self, input_data):
##        if self.input_data is None:
##            raise error('no input data')
        images = ImagesContainer()
        images.handle = pygadgetron.cGT_processImages\
             (self.handle, input_data.handle)
        _check_status(images.handle)
        return images
##    def get_output(self):
##        images = ImagesContainer()
##        images.handle = pygadgetron.cGT_reconstructedImagesList(self.handle)
##        _check_status(images.handle)
##        return images

class AcquisitionsProcessor(GadgetChain):
    def __init__(self):
        self.handle = None
        self.handle = pygadgetron.cGT_newObject('AcquisitionsProcessor')
        _check_status(self.handle)
        self.input_data = None
    def __del__(self):
        if self.handle is not None:
            pygadgetron.deleteObject(self.handle)
    def process(self, input_data):
        acquisitions = AcquisitionsContainer()
        acquisitions.handle = pygadgetron.cGT_processAcquisitions\
             (self.handle, input_data.handle)
        _check_status(acquisitions.handle)
        return acquisitions

##class RemoveOversamplingProcessor(AcquisitionsProcessor):
##    def __init__(self):
##        self.handle = None
##        self.handle = pygadgetron.cGT_newObject('RemoveOversamplingProcessor')
##        _check_status(self.handle)
##    def __del__(self):
##        if self.handle is not None:
##            #print('deleting acquisitions processor object...')
##            pygadgetron.deleteObject(self.handle)
    
class SimpleReconstructionProcessor(ImagesReconstructor):
    def __init__(self):
        self.handle = None
        self.handle = pygadgetron.cGT_newObject('SimpleReconstructionProcessor')
        _check_status(self.handle)
        self.input_data = None
    def __del__(self):
        if self.handle is not None:
            pygadgetron.deleteObject(self.handle)
    
##class ExtractRealImagesProcessor(ImagesProcessor):
##    def __init__(self):
##        self.handle = None
##        self.handle = pygadgetron.cGT_newObject('ExtractRealImagesProcessor')
##        _check_status(self.handle)
##    def __del__(self):
##        if self.handle is not None:
##            pygadgetron.deleteObject(self.handle)
    
def MR_remove_x_oversampling(input_data):
##    acq_proc = RemoveOversamplingProcessor()
##    output_data = acq_proc.process(input_data)
    handle = pygadgetron.cGT_newObject('RemoveOversamplingProcessor')
    _check_status(handle)
    output_data = AcquisitionsContainer()
    output_data.handle = pygadgetron.cGT_processAcquisitions\
         (handle, input_data.handle)
    _check_status(output_data.handle)
    pygadgetron.deleteObject(handle)
    return output_data

def MR_extract_real_images(complex_images):
##    img_proc = ExtractRealImagesProcessor()
##    real_images = img_proc.process(complex_images)
    handle = pygadgetron.cGT_newObject('ExtractRealImagesProcessor')
    _check_status(handle)
    real_images = ImagesContainer()
    real_images.handle = pygadgetron.cGT_processImages\
         (handle, complex_images.handle)
    _check_status(real_images.handle)
    pygadgetron.deleteObject(handle)
    return real_images
